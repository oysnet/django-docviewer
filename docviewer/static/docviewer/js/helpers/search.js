_.extend(docviewer.Schema.helpers, {
  getSearchResponse: function(query){
    var handleResponse = docviewer.jQuery.proxy(function(response){
      this.viewer.searchResponse = response;
      var hasResults = (response.results.length > 0) ? true : false;

      var text = hasResults ? 'of '+response.results.length + ' ' : ' ';
      this.viewer.$('span.docviewer-totalSearchResult').text(text);
      this.viewer.$('span.docviewer-searchQuery').text(response.query);
      if (hasResults) {
        // this.viewer.history.save('search/p'+response.results[0]+'/'+response.query);
        var currentPage = this.viewer.models.document.currentPage();
        var page = (_.include(response.results, currentPage)) ? currentPage : response.results[0];
        this.events.loadText(page - 1, this.highlightSearchResponses);
      } else {
        this.highlightSearchResponses();
      }
    }, this);

    var failResponse = function() {
      this.viewer.$('.docviewer-currentSearchResult').text('Search is not available at this time');
      this.viewer.$('span.docviewer-searchQuery').text(query);
      this.viewer.$('.docviewer-searchResults').addClass('docviewer-noResults');
    };

    var searchURI = this.viewer.schema.document.resources.search.replace('{query}', encodeURIComponent(query));
    if (this.viewer.helpers.isCrossDomain(searchURI)) searchURI += '&callback=?';
    docviewer.jQuery.ajax({url : searchURI, dataType : 'json', success : handleResponse, error : failResponse});
  },
  acceptInputCallBack: function(){
    var pageIndex = parseInt(this.elements.currentPage.text(),10) - 1;
    // sanitize input

    pageIndex       = (pageIndex === '') ? 0 : pageIndex;
    pageIndex       = (pageIndex < 0) ? 0 : pageIndex;
    pageIndex       = (pageIndex+1 > this.models.document.totalPages) ? this.models.document.totalPages-1 : pageIndex;
    var pageNumber  = pageIndex+1;

    this.elements.currentPage.text(pageNumber);
    this.viewer.$('.docviewer-pageNumberContainer input').val(pageNumber);

    if(this.viewer.state === 'ViewDocument' ||
       this.viewer.state === 'ViewThumbnails'){
      // this.viewer.history.save('document/p'+pageNumber);
      this.jump(pageIndex);
    }else if(this.viewer.state === 'ViewText'){
      // this.viewer.history.save('text/p'+pageNumber);
      this.events.loadText(pageIndex);
    }

  },
  highlightSearchResponses: function(){

    var viewer    = this.viewer;
    var response  = viewer.searchResponse;

    if(!response) return false;

    var results         = response.results;
    var currentResultEl = this.viewer.$('.docviewer-currentSearchResult');

    if (results.length == 0){
      currentResultEl.text('No Results');
      this.viewer.$('.docviewer-searchResults').addClass('docviewer-noResults');
    }else{
      this.viewer.$('.docviewer-searchResults').removeClass('docviewer-noResults');
    }
    for(var i = 0; i < response.results.length; i++){
      if(this.models.document.currentPage() === response.results[i]){
        currentResultEl.text('Page ' + (i+1) + ' ');
        break;
      }
    }

    // Replaces spaces in query with `\s+` to match newlines in textContent,
    // escape regex char contents (like "()"), and only match on word boundaries.
    var query             = '\\b' + response.query.replace(/[-[\]{}()*+?.,\\^$|#]/g, "\\$&").replace(/\s+/g, '\\s+') + '\\b';
    var textContent       = this.viewer.$('.docviewer-textContents');
    var currentPageText   = textContent.text();
    var pattern           = new RegExp(query,"ig");
    var replacement       = currentPageText.replace(pattern,'<span class="docviewer-searchMatch">$&</span>');

    textContent.html(replacement);

    var highlightIndex = (viewer.toHighLight) ? viewer.toHighLight : 0;
    this.highlightMatch(highlightIndex);

    // cleanup
    currentResultEl = null;
    textContent     = null;

  },
  // Highlight a single instance of an entity on the page. Make sure to
  // convert into proper UTF8 before trying to get the entity length, and
  // then back into UTF16 again.
  highlightEntity: function(offset, length) {
    this.viewer.$('.docviewer-searchResults').addClass('docviewer-noResults');
    var textContent = this.viewer.$('.docviewer-textContents');
    var text        = textContent.text();
    var pre         = text.substr(0, offset);
    var entity      = text.substr(offset, length);
    var post        = text.substr(offset + length);
    text            = [pre, '<span class="docviewer-searchMatch">', entity, '</span>', post].join('');
    textContent.html(text);
    this.highlightMatch(0);
  },

  highlightMatch: function(index){
    var highlightsOnThisPage   = this.viewer.$('.docviewer-textContents span.docviewer-searchMatch');
    if (highlightsOnThisPage.length == 0) return false;
    var currentPageIndex    = this.getCurrentSearchPageIndex();
    var toHighLight         = this.viewer.toHighLight;

    if(toHighLight){
      if(toHighLight !== false){
        if(toHighLight === 'last'){
          index = highlightsOnThisPage.length - 1;
        }else if(toHighLight === 'first'){
          index = 0;
        }else{
          index = toHighLight;
        }
      }
      toHighLight = false;
    }
    var searchResponse = this.viewer.searchResponse;
    if (searchResponse) {
      if(index === (highlightsOnThisPage.length)){

        if(searchResponse.results.length === currentPageIndex+1){
          return;
        }
        toHighLight = 'first';
        this.events.loadText(searchResponse.results[currentPageIndex + 1] - 1,this.highlightSearchResponses);

        return;
      }else if(index === -1){
        if(currentPageIndex-1 < 0){
          return  false;
        }
        toHighLight = 'last';
        this.events.loadText(searchResponse.results[currentPageIndex - 1] - 1,this.highlightSearchResponses);

        return;
      }
      highlightsOnThisPage.removeClass('docviewer-highlightedMatch');
    }

    var match = this.viewer.$('.docviewer-textContents span.docviewer-searchMatch:eq('+index+')');
    match.addClass('docviewer-highlightedMatch');

    this.elements.window[0].scrollTop = match.position().top - 50;
    if (searchResponse) searchResponse.highlighted = index;

    // cleanup
    highlightsOnThisPage = null;
    match = null;
  },
  getCurrentSearchPageIndex: function(){
    var searchResponse = this.viewer.searchResponse;
    if(!searchResponse) {
      return false;
    }
    var docModel = this.models.document;
    for(var i = 0,len = searchResponse.results.length; i<len;i++){
      if(searchResponse.results[i] === docModel.currentPage()){
        return i;
      }
    }
  },
  highlightPreviousMatch: function(e){
    e.preventDefault();
    this.highlightMatch(this.viewer.searchResponse.highlighted-1);
  },
  highlightNextMatch: function(e){
    e.preventDefault(e);
    this.highlightMatch(this.viewer.searchResponse.highlighted+1);
  },

  clearSearch: function(e) {
    this.elements.searchInput.val('').keyup().focus();
  },

  showEntity: function(name, offset, length) {
    this.viewer.$('span.docviewer-totalSearchResult').text('');
    this.viewer.$('span.docviewer-searchQuery').text(name);
    this.viewer.$('span.docviewer-currentSearchResult').text("Searching");
    this.events.loadText(this.models.document.currentIndex(), _.bind(this.viewer.helpers.highlightEntity, this.viewer.helpers, offset, length));
  },
  cleanUpSearch: function(){
    var viewer            = this.viewer;
    viewer.searchResponse = null;
    viewer.toHighLight    = null;
    if (this.elements) this.elements.searchInput.keyup().blur();
  }

});