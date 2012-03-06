_.extend(docviewer.Schema.events, {
  handleNavigation: function(e){
    var el          = this.viewer.$(e.target);
    var triggerEl   = el.closest('.docviewer-trigger');
    var noteEl      = el.closest('.docviewer-annotationMarker');
    var chapterEl   = el.closest('.docviewer-chapter');
    if (!triggerEl.length) return;

    if (el.hasClass('docviewer-expander')) {
      return chapterEl.toggleClass('docviewer-collapsed');

    }else if (noteEl.length) {
      var aid         = noteEl[0].id.replace('docviewer-annotationMarker-','');
      var annotation  = this.models.annotations.getAnnotation(aid);
      var pageNumber  = parseInt(annotation.index,10)+1;

      if(this.viewer.state === 'ViewText'){
        this.loadText(annotation.index);

        // this.viewer.history.save('text/p'+pageNumber);
      }else{
        if (this.viewer.state === 'ViewThumbnails') {
          this.viewer.open('ViewDocument');
        }
        this.viewer.pageSet.showAnnotation(annotation);
      }

    } else if (chapterEl.length) {
      // its a header, take it to the page
      chapterEl.removeClass('docviewer-collapsed');
      var cid           = parseInt(chapterEl[0].id.replace('docviewer-chapter-',''), 10);
      var chapterIndex  = parseInt(this.models.chapters.getChapterPosition(cid),10);
      var pageNumber    = parseInt(chapterIndex,10)+1;

      if(this.viewer.state === 'ViewText'){
        this.loadText(chapterIndex);
        // this.viewer.history.save('text/p'+pageNumber);
      }else if(this.viewer.state === 'ViewDocument' ||
               this.viewer.state === 'ViewThumbnails'){
        this.helpers.jump(chapterIndex);
        // this.viewer.history.save('document/p'+pageNumber);
        if (this.viewer.state === 'ViewThumbnails') {
          this.viewer.open('ViewDocument');
        }
      }else{
        return false;
      }

    }else{
      return false;
    }
  }
});