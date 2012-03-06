// Fake out console.log for safety, if it doesn't exist.
window.console || (window.console = {});
console.log    || (console.log = _.identity);

// Create the docviewer namespaces.
window.docviewer   = window.docviewer   || {};
docviewer.jQuery   = jQuery.noConflict(true);
docviewer.viewers  = docviewer.viewers  || {};
docviewer.model    = docviewer.model    || {};

