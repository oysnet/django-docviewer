/*global alert,docviewer,reload_url,$*/
/*global Ext*/
/*global Jed*/
/*global i18n*/
/*global FBL*/
/*global DEBUG*/
/*global yepnope*/
/*global PhoneGap*/
/*global MathJax*/
/*global JSON*/
/*global console*/
/*global printStackTrace*/
/*global head*/
/*global jQuery*/
/*jslint forin:true, noarg:true, noempty:true, eqeqeq:true, bitwise:true, strict:false, undef:true, curly:true, browser:true, indent:2, maxerr:50
*/


var docviewer_cover = "";
(function () {
  "use strict";

  function animate_fixed(message) {
    $("#fixed-div").html(message);
    $("#fixed-div").fadeIn(1000);
    $("#fixed-div").delay(2000);
    $("#fixed-div").fadeOut(2000);
  }

  function get_coord(anno, cover) {
    var zoomfactor = mydocviewer.models.pages.zoomFactor(),
      cover_width = cover.width(),
      cover_height = cover.height(),
      anno_offsetX = anno.position().left,
      anno_offsetY = anno.position().top,
      y_initial = 5 + Math.round((anno_offsetY) / zoomfactor),
      y_end =   5 + Math.round((anno_offsetY + anno.height()) / zoomfactor),
      x_initial = 7 + Math.round((anno_offsetX) / zoomfactor),
      x_end =   16 + Math.round((anno_offsetX + anno.width()) / zoomfactor);
    return y_initial + "," + x_end + "," + y_end + "," + x_initial;
  }

  function add_annotation(title, content, location, page_id) {
    var adata = { };
    adata.title = title;
    adata.content = content;
    adata.location = location;
    adata.page_id = page_id;
    $.ajax({
      url: "add_annotation/",
      data: adata,
      success: function (payload) {
        var current_page = mydocviewer.api.currentPage(),
        zoomLevel = mydocviewer.models.pages.zoomLevel;
        console.log(zoomLevel);
        mydocviewer = docviewer.load(reload_url,
          { container: '#documentviewer-container',
            afterLoad: function(){
              //this.pageSet.zoom({zoomLevel: zoomLevel });
              mydocviewer.api.setCurrentPage(current_page);
              animate_fixed("Annotation saved");
            }
          });
      },
      dataType: 'json',
      error: function (payload) {
        alert("Error en el ajax request");
      },
      type: 'GET'
    });
  }

  function enable_edition_mode() {
    $('#add-annotation').hide();
    $('#cancel-annotation').show();
    $('.docviewer-annotations').hide();
    mydocviewer.dragReporter.unBind();
    $('.docviewer-cover').live('click', function (ev) {
      var docviewer_set = $(ev.target).parents('.docviewer-set'),
        selection_area = $('#annotation-area');
      if (ev.target.className === 'docviewer-cover') {
        docviewer_cover = $(ev.target);
      } else {
        docviewer_cover = $(ev.target).parents('.docviewer-cover');
      }
      $("#fixed-div").show();
      if (selection_area.length === 0) {
        selection_area = jQuery('<div/>', {
          id: 'annotation-area',
          html: '<span id="instruction"> Drag and resize me</span>'
        }).resizable().draggable();
      }
      docviewer_cover.prepend(selection_area);
      selection_area.css('top', ev.offsetY);
      selection_area.css('left', ev.offsetX);
      selection_area.css('position', 'absolute');
    });
    $('#annotation-button').live('click', function (ev) {
      ev.preventDefault();
      var selection_area = $('#annotation-area');
      add_annotation($('#annotation-title').val(),
        $('#annotation-content').val(),
        get_coord(selection_area,
          selection_area.parents('.docviewer-cover')),
          mydocviewer.api.currentPage());
    });
    $('#form-annotation').show();
  }

  function disable_edition_mode() {
    $('#add-annotation').show();
    $('#cancel-annotation').hide();
    $('.docviewer-annotations').show();
    $('.docviewer-pages').css('overflow', 'auto');
    $('.docviewer-cover').die('click');
    $('#annotation-area').remove();
    $('#form-annotation').hide();
    mydocviewer.dragReporter.setBinding();
  }

  function update_anotation(id, field, value) {
    var adata = { };
    adata.id = id;
    adata[field] = value;
    $.ajax({
      type: "GET",
      url: "update_annotation/",
      data: adata,
      success: function (payload) {
        animate_fixed("Annotation updated");
      },
      dataType: 'json',
      error: function (payload) {
        animate_fixed("Error en el ajax request");
      }
    });
  }


  $(document).ready(function () {
    var title = "",
      content = "";
    $('div.docviewer-annotationBody').live('click', function (ev) {
      content = ev.target.innerText;
      ev.target.contentEditable = 'true';
      $(ev.target).focus();
    });
    $('.docviewer-annotationBody').live('blur', function (ev) {
      if (content !== ev.target.innerText) {
        update_anotation(ev.target.parentElement.parentElement.dataset.id,
          'content', ev.target.innerText);
      }
      ev.target.contentEditable = 'false';
    });
    $('.docviewer-annotationBody').live('keypress', function (ev) {
      if (ev.keyCode === 13) {
        ev.target.blur();
      }
    });
    $('.docviewer-annotationTitle').live('click', function (ev) {
      title = ev.target.innerText;
      ev.target.contentEditable = 'true';
      $(ev.target).focus();
    });
    $('.docviewer-annotationTitle').live('blur', function (ev) {
      if (title !== ev.target.innerText) {
        update_anotation(
          $(ev.target).parents(".docviewer-annotation")[0].dataset.id,
          'title',
          ev.target.innerText
        );
        ev.target.contentEditable = 'false';
      }
    });
    $('.docviewer-annotationTitle').live('keypress', function (ev) {
      if (ev.keyCode === 13) {
        ev.target.blur();
      }
    });
    $("#add-annotation").live('click', function (ev) {
      enable_edition_mode();
    });
    $("#cancel-annotation").live('click', function (ev) {
      disable_edition_mode();
    });
    $(".docviewer-remove").live('click', function (ev) {
      var adata = { };
      adata.id = $(ev.target).parents(".docviewer-annotation")[0].dataset.id;
      $.ajax({
        url: "remove_annotation/",
        data: adata,
        success: function (payload) {
          var current_page = mydocviewer.api.currentPage();
          mydocviewer = docviewer.load(reload_url,
            { container: '#documentviewer-container',
              afterLoad: function(){
                mydocviewer.api.setCurrentPage(current_page)
              }
            });
        },
        dataType: 'json',
        type: 'GET'
      });
    });
  });
}());


