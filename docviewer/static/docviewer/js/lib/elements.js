docviewer.Elements = function(viewer){
  this._viewer = viewer;
  var elements = docviewer.Schema.elements;
  for (var i=0, elemCount=elements.length; i < elemCount; i++) {
    this.getElement(elements[i]);
  }
};

// Get and store an element reference
docviewer.Elements.prototype.getElement = function(elementQuery,force){
  this[elementQuery.name] = this._viewer.$(elementQuery.query);
};
