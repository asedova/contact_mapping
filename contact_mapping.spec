/*
A KBase module: contact_mapping
*/

module contact_mapping {
    typedef structure {
        string report_name;
        string report_ref;
    } ReportResults;

    /*
        This example function accepts any number of parameters and returns results in a KBaseReport
    */
    funcdef run_contact_mapping(mapping<string,UnspecifiedObject> params) returns (ReportResults output) authentication required;

};