# -*- coding: utf-8 -*-
#BEGIN_HEADER
import uuid
import logging
import os
from subprocess import Popen
import subprocess
from subprocess import PIPE, STDOUT
import sys
from installed_clients.KBaseReportClient import KBaseReport
from installed_clients.MSAUtilsClient import MSAUtils
from installed_clients.ProteinStructureUtilsClient import ProteinStructureUtils
#END_HEADER


class contact_mapping:
    '''
    Module Name:
    contact_mapping

    Module Description:
    A KBase module: contact_mapping
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = "https://github.com/asedova/contact_mapping"
    GIT_COMMIT_HASH = "a9dbd3aa2b7a6a41c81690d00438011f11d3abfe"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.shared_folder = config['scratch']
        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)
        #END_CONSTRUCTOR
        pass


    def run_contact_mapping(self, ctx, params):
        """
        This example function accepts any number of parameters and returns results in a KBaseReport
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "ReportResults" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        
        # ctx is the context object
        # return variables are: output
        #BEGIN run_contact_mapping
        msa_utl = MSAUtils(self.callback_url,service_ver='dev')

        ccmpred_command_list = ['ccmpred', '--num-threads', '4',  '--ofn-pll', ]
        msa = msa_utl.msa_to_fasta_file( {'destination_dir': self.shared_folder, 
                             'input_ref': params['msa_ref']})
        msa=msa['file_path']
        ccmpred_command_list += [msa]
        name= params.get('contactmap_name')
        ccmpred_command_list += ['-m',  f'{self.shared_folder}/{name}.noapc.mat',
                '--apc', f'{self.shared_folder}/{name}.apc.mat',
                '--entropy-correction', f'{self.shared_folder}/{name}.ec.mat']

        if params.get('max_gaps_per_position'):
            ccmpred_command_list +=['--max-gap-pos', params.get('max_gaps_per_position')]
        if params.get('max_gaps_per_sequence'):
            ccmpred_command_list +=['--max-gap-seq', params.get('max_gaps_per_sequence')]

        with Popen(ccmpred_command_list, stdout=PIPE, stderr=STDOUT, bufsize=1) as p:  

            with open(self.shared_folder + '/ccmpred_out.txt', 'wb') as f:
                for line in p.stdout:
                    f.write(line)
                    sys.stdout.buffer.write(line)
                    sys.stdout.buffer.flush()


        ccm_plot_cmd_list= ['ccm_plot', 'cmap', '--mat-file', f'{self.shared_folder}/{name}.apc.mat', 
               '--alignment-file', msa, '--plot-file', 
                f'{self.shared_folder}/{name}.apc.html', '--seq-sep', '4', 
                '--contact-threshold', '8'] 
  
        if params.get('pdb_ref'):
            pdb_utl = ProteinStructureUtils(self.callback_url,service_ver='dev')
            pdb = pdb_utl.structure_to_pdb_file( {'destination_dir': self.shared_folder, 
                             'input_ref': params['pdb_ref']})
            pdb=pdb['file_path']          
            ccm_plot_cmd_list+=['--pdb-file', pdb]
           
        Popen(ccm_plot_cmd_list, stdout=sys.stdout, stderr=sys.stderr).communicate()        

        report_params = {'message': 'you successfully ran ccmpred', 
                          'html_links': [
                          {'path': f'{self.shared_folder}/{name}.apc.html', 'name': 
                           f'{name}.apc.html', 'description': 'plot of contact map'}
                          ],
                          'direct_html_link_index': 0,
                          'workspace_name': params['workspace_name'],
                          'report_object_name': 'ccmpred_report' + str(uuid.uuid4()),
                          'file_links': [
                          {'path': f'{self.shared_folder}/{name}.noapc.mat', 
                           'name': f'{name}.noapc.mat', 
                           'description':  'summed score matrix, uncorrected'}, 

                          {'path': f'{self.shared_folder}/{name}.apc.mat',
                           'name':f'{name}.apc.mat',
                           'description': 'summed score matrix, APC-corrected'},        

                          {'path': f'{self.shared_folder}/{name}.ec.mat',
                           'name': f'{name}.ec.mat',
                           'description': 'summed score matrix, entropy-bias corrected'}
                          ]
                        }
 
        report = KBaseReport(self.callback_url)
        report_info = report.create_extended_report(report_params)
                                               
        output = {
            'report_name': report_info['name'],
            'report_ref': report_info['ref'],
        }
        #END run_contact_mapping

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method run_contact_mapping return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
