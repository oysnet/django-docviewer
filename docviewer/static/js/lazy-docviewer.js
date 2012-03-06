$(window).load(function() {
			var docviewer_index = 0;
			var targeting = {};
      this.viewer.$.support.cors
			$('.docviewer').each(function() {
						if (typeof($(this).attr('id')) === 'undefined') {
							$(this).attr('id', 'docviewer-' + docviewer_index);
							var id = $(this).attr('id');
							docviewer_index++;
						} else {
							var id = $(this).attr('id');
						}
            docviewer.load('/documents/doc-'+$(this).attr('data-document')+'.json', {
									container : '#'+id,
                  width: '100%',
                  height: 700,
                  text: true,
                  search: true,
									sidebar : false
								});
					});
		});
