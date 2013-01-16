$(document).ready(function(){
    $('div.docviewer-annotationBody').live('click', function(ev){
        ev.target.contentEditable='true';
    });
    $('.docviewer-annotationBody').live('blur', function(ev){
      update_anotation(
          ev.target.parentElement.parentElement.dataset.id, 
          'content', ev.target.innerText)
      ev.target.contentEditable='false';
    });
    $('.docviewer-annotationTitle').live('click', function(ev){
        ev.target.contentEditable='true';
    });
    $('.docviewer-annotationTitle').live('blur', function(ev){
      update_anotation(
          ev.target.parentElement.parentElement.parentElement.dataset.id, 
          'title', ev.target.innerText)
      ev.target.contentEditable='false';
    });
});

function update_anotation(id, field, value){
    adata = { }
    adata['id'] = id 
    adata[field] = value
    $.ajax({
      type: "GET",
      url: "update_annotation/",
      data: adata
    }).done(function( payload ) {
      alert( "Data Saved: " + payload[status] );
    });
}


