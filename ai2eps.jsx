// Save AI as EPS
var folder = Folder.selectDialog("Select Source Folder..."); // select folder
if (folder==null) {
  alert("Good Bye");
}
else {
  var files = find_files (folder, ['.ai']);
  var fileCount = files.length; // count them
  if (fileCount>0) {
    for (i=0; i<fileCount; i++) {
      var idoc = app.open(files[i]);
      var saveOpts = new EPSSaveOptions();
      saveOpts.pdfCompatible = true;
      idoc.saveAs( files[i], saveOpts );
      idoc.close();
    }
    alert(fileCount + ' file(s) processed');
  }
  else {
    alert("There are no Illustrator files in this folder.");
  }
}

function find_files (dir, mask_array){
  var arr = [];
  for (var i = 0; i < mask_array.length; i++){
    arr = arr.concat (find_files_sub (dir, [], mask_array[i].toUpperCase()));
  }
  return arr;
}

function find_files_sub (dir, array, mask){
  var f = Folder (dir).getFiles ( '*.*' );
  for (var i = 0; i < f.length; i++){
    if (f[i] instanceof Folder){
      find_files_sub (f[i], array, mask);
    } else if (f[i].name.substr (-mask.length).toUpperCase() == mask){
            array.push (f[i]);
    }
  }
  return array;
}