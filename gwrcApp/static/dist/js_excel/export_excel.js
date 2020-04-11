jQuery.noConflict();
(function( $ ) {
  $(function() {
$("#exporttable").click(function(e){
var table = $("#htmltable");
if(table && table.length){
$(table).table2excel({
exclude: ".noExl",
name: "Excel Document Name",
filename: "list_IMEI" + new Date().toISOString().replace(/[\-\:\.]/g, "") + ".xls",
fileext: ".xls",
exclude_img: true,
exclude_links: true,
exclude_inputs: true,
preserveColors: false
});
}
});

});
})(jQuery);


jQuery.noConflict();
(function( $ ) {
  $(function() {
$("#exporttable1").click(function(e){
var table = $("#htmltable1");
if(table && table.length){
$(table).table2excel({
exclude: ".noExl",
name: "Excel Document Name",
filename: "list_Agent" + new Date().toISOString().replace(/[\-\:\.]/g, "") + ".xls",
fileext: ".xls",
exclude_img: true,
exclude_links: true,
exclude_inputs: true,
preserveColors: false
});
}
});

});
})(jQuery);


jQuery.noConflict();
(function( $ ) {
  $(function() {
$("#exporttable2").click(function(e){
var table = $("#htmltable2");
if(table && table.length){
$(table).table2excel({
exclude: ".noExl",
name: "Excel Document Name",
filename: "list_Msisdn" + new Date().toISOString().replace(/[\-\:\.]/g, "") + ".xls",
fileext: ".xls",
exclude_img: true,
exclude_links: true,
exclude_inputs: true,
preserveColors: false
});
}
});

});
})(jQuery);


jQuery.noConflict();
(function( $ ) {
  $(function() {
$("#exporttable3").click(function(e){
var table = $("#htmltable3");
if(table && table.length){
$(table).table2excel({
exclude: ".noExl",
name: "Excel Document Name",
filename: "list_mobile" + new Date().toISOString().replace(/[\-\:\.]/g, "") + ".xls",
fileext: ".xls",
exclude_img: true,
exclude_links: true,
exclude_inputs: true,
preserveColors: false
});
}
});

});
})(jQuery);