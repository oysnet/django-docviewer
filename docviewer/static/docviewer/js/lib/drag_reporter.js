docviewer.DragReporter = function(viewer, toWatch, dispatcher, argHash) {
  this.viewer         = viewer;
  this.dragClassName  = 'docviewer-dragging';
  this.sensitivityY   = 1.0;
  this.sensitivityX   = 1.0;
  this.oldPageY       = 0;

  _.extend(this, argHash);

  this.dispatcher             = dispatcher;
  this.toWatch                = this.viewer.$(toWatch);
  this.boundReporter          = _.bind(this.mouseMoveReporter,this);
  this.boundMouseUpReporter   = _.bind(this.mouseUpReporter,this);
  this.boundMouseDownReporter = _.bind(this.mouseDownReporter,this);

  this.setBinding();
};

docviewer.DragReporter.prototype.shouldIgnore = function(e) {
  if (!this.ignoreSelector) return false;
  var el = this.viewer.$(e.target);
  return el.parents().is(this.ignoreSelector) || el.is(this.ignoreSelector);
};

docviewer.DragReporter.prototype.mouseUpReporter     = function(e){
  if (this.shouldIgnore(e)) return true;
  e.preventDefault();
  clearInterval(this.updateTimer);
  this.stop();
};

docviewer.DragReporter.prototype.oldPositionUpdater   = function(){
  this.oldPageY = this.pageY;
};

docviewer.DragReporter.prototype.stop         = function(){
  this.toWatch.removeClass(this.dragClassName);
  this.toWatch.unbind('mousemove');
};

docviewer.DragReporter.prototype.setBinding         = function(){
  this.toWatch.mouseup(this.boundMouseUpReporter);
  this.toWatch.mousedown(this.boundMouseDownReporter);
};

docviewer.DragReporter.prototype.unBind           = function(){
  this.toWatch.unbind('mouseup',this.boundMouseUpReporter);
  this.toWatch.unbind('mousedown',this.boundMouseDownReporter);
};

docviewer.DragReporter.prototype.destroy           = function(){
  this.unBind();
  this.toWatch = null;
};

docviewer.DragReporter.prototype.mouseDownReporter   = function(e){
   if (this.shouldIgnore(e)) return true;
  e.preventDefault();
  this.pageY    = e.pageY;
  this.pageX    = e.pageX;
  this.oldPageY = e.pageY;

  this.updateTimer = setInterval(_.bind(this.oldPositionUpdater,this),1200);

  this.toWatch.addClass(this.dragClassName);
  this.toWatch.mousemove(this.boundReporter);
};

docviewer.DragReporter.prototype.mouseMoveReporter     = function(e){
  if (this.shouldIgnore(e)) return true;
  e.preventDefault();
  var deltaX      = Math.round(this.sensitivityX * (this.pageX - e.pageX));
  var deltaY      = Math.round(this.sensitivityY * (this.pageY - e.pageY));
  var directionX  = (deltaX > 0) ? 'right' : 'left';
  var directionY  = (deltaY > 0) ? 'down' : 'up';
  this.pageY      = e.pageY;
  this.pageX      = e.pageX;
  if (deltaY === 0 && deltaX === 0) return;
  this.dispatcher({ event: e, deltaX: deltaX, deltaY: deltaY, directionX: directionX, directionY: directionY });
};
