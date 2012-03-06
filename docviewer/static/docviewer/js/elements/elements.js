// We cache DOM references to improve speed and reduce DOM queries
docviewer.Schema.elements =
[
  { name: 'browserDocument',    query: document },
  { name: 'browserWindow',      query: window },
  { name: 'header',             query: 'div.docviewer-header'},
  { name: 'viewer',             query: 'div.docviewer-docViewer'},
  { name: 'window',             query: 'div.docviewer-pages'},
  { name: 'sets',               query: 'div.docviewer-set'},
  { name: 'pages',              query: 'div.docviewer-page'},
  { name: 'metas',              query: 'div.docviewer-pageMeta'},
  { name: 'bar',                query: 'div.docviewer-bar'},
  { name: 'currentPage',        query: 'span.docviewer-currentPage'},
  { name: 'well',               query: 'div.docviewer-well'},
  { name: 'collection',         query: 'div.docviewer-pageCollection'},
  { name: 'annotations',        query: 'div.docviewer-allAnnotations'},
  { name: 'navigation',         query: 'div.docviewer-navigation' },
  { name: 'chaptersContainer',  query: 'div.docviewer-chaptersContainer' },
  { name: 'searchInput',        query: 'input.docviewer-searchInput' },
  { name: 'textCurrentPage',    query: 'span.docviewer-textCurrentPage' },
  { name: 'coverPages',         query: 'div.docviewer-cover' },
  { name: 'fullscreen',         query: 'div.docviewer-fullscreen' }
];