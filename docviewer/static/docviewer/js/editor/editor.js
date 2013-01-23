$(document).ready(function(){
    //$( "#add-annotation" ).resizable().draggable()
    //$( "#add-annotation" ).innerText("hola")
    title = ""
    content = ""
    $('div.docviewer-annotationBody').live('click', function(ev){
        content = ev.target.innerText
        ev.target.contentEditable='true'
        $(ev.target).focus()
    })
    $('.docviewer-annotationBody').live('blur', function(ev){
      if (content != ev.target.innerText)
        update_anotation(
            ev.target.parentElement.parentElement.dataset.id, 
            'content', ev.target.innerText)
      ev.target.contentEditable='false'
    })
    $('.docviewer-annotationBody').live('keypress', function(ev){
      if (ev.keyCode == 13) {
        ev.target.blur()
      }
    })
    $('.docviewer-annotationTitle').live('click', function(ev){
        title = ev.target.innerText
        ev.target.contentEditable='true'
        $(ev.target).focus()
    })
    $('.docviewer-annotationTitle').live('blur', function(ev){
      if (title != ev.target.innerText)
        update_anotation(
            $(ev.target).parents(".docviewer-annotation")[0].dataset.id, 
            'title', ev.target.innerText)
      ev.target.contentEditable='false'
    })
    $('.docviewer-annotationTitle').live('keypress', function(ev){
      if (ev.keyCode == 13) {
        ev.target.blur()
      }
    })
    $( "#add-annotation" ).live('click', function(ev){
      enable_edition_mode()
    })
    $( "#cancel-annotation" ).live('click', function(ev){
      disable_edition_mode()
    })
    $( ".docviewer-remove" ).live('click', function(ev){
      adata = { }
      adata['id'] = $(ev.target).parents(".docviewer-annotation")[0].dataset.id
      req = $.ajax({
          url: "remove_annotation/",
          data: adata,
          success: function (payload ) {
                   docviewer.load(reload_url, 
                              { container: '#documentviewer-container' })
                   animate_fixed("Annotation removed");
               },
          dataType: 'json',
          type: 'GET'})

    })

})

docviewer_cover = ""
function enable_edition_mode(){
    $('#add-annotation').hide()
    $('#cancel-annotation').show()

    $('.docviewer-annotations').hide()
//    $('.docviewer-pages').css('overflow', 'visible')

    $('.docviewer-cover').live('click', function(ev){

        docviewer_set = $(ev.target).parents('.docviewer-set')
        selection_area = $('#annotation-area')
        if (ev.target.className == 'docviewer-cover')
          docviewer_cover = $(ev.target)
        else
          docviewer_cover = $(ev.target).parents('.docviewer-cover')

        $("#fixed-div").show();
        if (selection_area.length == 0)
          selection_area = jQuery('<div/>', {
                            id: 'annotation-area',
                            html: '<span id="instruction"> Drag and resize me</span>'
                          }).resizable().draggable({
                              drag: function(ev){
                                $("#fixed-div").html(all_coords(selection_area,docviewer_cover,ev))
                              },
                              stop:function(){ 
                                  //alert(get_coord(selection_area,docviewer_cover))
                              }
                          })

        $("#fixed-div").html(all_coords(selection_area,docviewer_cover,ev))
        docviewer_cover.prepend(selection_area)
        selection_area.css('top',ev.offsetY)
        selection_area.css('left',ev.offsetX)
        selection_area.css('position','absolute')
        $("#fixed-div").append(all_coords(selection_area,docviewer_cover,ev))

    })
    
    $('#annotation-button').live('click', function(ev){
        ev.preventDefault()
        selection_area = $('#annotation-area')

        add_annotation($('#annotation-title').val(), 
                      $('#annotation-content').val(), 
                      get_coord(selection_area, 
                                selection_area.parents('.docviewer-cover')), 
                      parseInt(selection_area.parents('.docviewer-set')[0].dataset.id[1]) + 1)
    })
    
    $('#form-annotation').show()
}


function all_coords(annotation, cover, event){
    aoffset = annotation.offset()
    coffset = cover.offset()
    return "event.offsets: (" + event.offsetX + "," + event.offsetY +")" +
           "- event.pages: (" + event.pageX + "," + event.pageY +")" +
           "- event.clients: (" + event.clientX + "," + event.clientY +")" +
           "<br> annotation.offset: (" + aoffset.left + "," + aoffset.top +")" +
           " - cover.offset: (" + coffset.left + "," + coffset.top +")" 

}

function get_coord(annotation, cover){
    cover_width = cover.width()
    cover_height = cover.height()
    
    annotation_offsetX = annotation.position().left
    annotation_offsetY = annotation.position().top
    
    y_initial = Math.round(annotation_offsetY/cover_height * 820)
    x_end = Math.round((annotation_offsetX + annotation.width())/cover_width * 730)
    y_end = Math.round((annotation_offsetY + annotation.height())/cover_height * 820)
    x_initial = Math.round(annotation_offsetX/cover_width * 730)
    
    return y_initial + "," + x_end + "," + y_end + "," + x_initial
}


function disable_edition_mode(){
    $( '#add-annotation' ).show()
    $( '#cancel-annotation' ).hide()
    $('.docviewer-annotations').show()
    $('.docviewer-pages').css('overflow', 'auto')
    $('.docviewer-cover').die('click')
    $('#annotation-area').remove()
    $('#form-annotation').hide()
}

function update_anotation(id, field, value){
    adata = { }
    adata['id'] = id 
    adata[field] = value
    $.ajax({
      type: "GET",
      url: "update_annotation/",
      data: adata,
      success: function (payload ) {
         animate_fixed("Annotation updated");
       },
       dataType: 'json',
       error: function (payload ) {
         alert("Error en el ajax request")
       },
      type: 'GET'
    })
}

function add_annotation(title, content, location, page_id){
    adata = { }
    adata['title'] = title 
    adata['content'] = content
    adata['location'] = location
    adata['page_id'] = page_id
    req = $.ajax({
      url: "add_annotation/",
      data: adata,
      success: function (payload ) {
               docviewer.load(reload_url, 
                  { container: '#documentviewer-container' })
               animate_fixed("Annotation saved");
               disable_edition_mode()
           },
      dataType: 'json',
      error: function (payload ) {
                   alert("Error en el ajax request")
               },
      type: 'GET',})

}


function animate_fixed(message){
  $("#fixed-div").html(message);
  $("#fixed-div").fadeIn(1000);
  $("#fixed-div").delay(2000);
  $("#fixed-div").fadeOut(2000);
}
