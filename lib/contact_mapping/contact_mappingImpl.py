# -*- coding: utf-8 -*-
#BEGIN_HEADER
import uuid
import logging
import os
from subprocess import Popen
import sys
from installed_clients.KBaseReportClient import KBaseReport
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
        path = '/kb/module/data'        
        Popen(['ccmpred', '--num-threads', '4',  path + '/4FAZA.fas', '--ofn-pll', 
                '--plot-opt-progress', self.shared_folder + '/4faza.log.html',
                '-m',  self.shared_folder + '/4faza.noapc.mat', 
                '--apc', self.shared_folder + '/4faza.apc.mat',  
                '--entropy-correction', self.shared_folder + '/4faza.ec.mat'], 
                stdout = sys.stdout, stderr=sys.stderr).communicate() 

        Popen(['ccm_plot', 'cmap', '--mat-file', self.shared_folder + '/4faza.apc.mat', 
               '--alignment-file', path + '/4FAZA.fas', '--plot-file', 
                self.shared_folder + '/4faza.apc.html', '--seq-sep', '4', 
                '--contact-threshold', '8'], stdout = sys.stdout, stderr=sys.stderr).communicate() 

        report_params = {'message': 'you successfully ran ccmpred', 
                          'html_links': [
                          {'path': self.shared_folder + '/4faza.apc.html', 'name': 
                           '4faza.apc.html', 'description': 'plot of contact map'}
                          ],
                          'direct_html_link_index': 0,
                          'workspace_name': params['workspace_name'],
                          'report_object_name': 'ccmpred_report' + str(uuid.uuid4()),
                          'file_links': [
                          {'path': self.shared_folder + '/4faza.noapc.mat', 
                           'name': '4fazaf.noapc.mat', 
                           'description':  'summed score matrix, uncorrected'}, 

                          {'path': self.shared_folder + '/4faza.apc.mat',
                           'name':'/4faza.apc.mat',
                           'description': 'summed score matrix, APC-corrected'},        

                          {'path': self.shared_folder + '/4faza.ec.mat',
                           'name': '/4faza.ec.mat',
                           'description': 'summed score matrix, entropy-bias corrected'}
                            ]
                           }
 
        report = KBaseReport(self.callback_url)
        report_info = report.create({'report': {'objects_created':[],
                                                'text_message': params['parameter_1']},
                                                'workspace_name': params['workspace_name']})
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
