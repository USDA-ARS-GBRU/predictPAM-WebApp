$(document).ready(function () {
  $('#table_id').DataTable({
    bProcessing: true,
    bServerSide: true,
    sPaginationType: "full_numbers",
    lengthMenu: [[10, 25, 50, 100], [10, 25, 50, 100]],
    bjQueryUI: true,
    sAjaxSource: '/serverside?a=b',
    columns: [
    
      {"data":"accession_x"}, 
{"data":      "accession_y"}, 
{"data":      "db_xref_x"}, 
{"data":      "db_xref_y"}, 
 {"data":     "distaltopam"}, 
 {"data":     "distance_x"}, 
  {"data":    "distance_y"}, 
  {"data":    "gene_synonym_x"}, 
  {"data":    "gene_synonym_y"}, 
   {"data":   "locus_tag_x"}, 
   {"data":   "locus_tag_y"}, 
   {"data":   "name_x"}, 
 {"data":     "name_y"}, 
 {"data":     "note_x"}, 
 {"data":     "note_y"}, 
  {"data":    "pam_seq"}, 
  {"data":    "product_name_confidence_x"}, 
  {"data":    "product_name_confidence_y"}, 
  {"data":    "product_synonym_x"}, 
  {"data":    "product_synonym_y"}, 
  {"data":    "product_x"}, 
  {"data":    "product_y"}, 
 {"data":     "protein_id_x"}, 
  {"data":    "protein_id_y"}, 
  {"data":    "proxitopam"}, 
  {"data":    "seqid"}, 
  {"data":    "start_x"}, 
  {"data":    "start_y"}, 
  {"data":    "stop_x"}, 
  {"data":    "stop_y"}, 
  {"data":    "strand"}, 
  {"data":    "strand_for_feature_x"}, 
  {"data":    "strand_for_feature_y"}, 
  {"data":    "target"}, 
  {"data":    "target_ep"}, 
 {"data":     "target_sp"}, 
  {"data":    "translation_x"}, 
  {"data":    "translation_y"}, 
  {"data":    "type_x"}, 
   {"data":   "type_y"}
    ]
  });
});