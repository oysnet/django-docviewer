$(window).load(function() {
			var docviewer_index = 0;
			var targeting = {};
      console.log('rrrr');
			$('.docviewer').each(function() {
        console.log('rr');
						if (typeof($(this).attr('id')) === 'undefined') {
							$(this).attr('id', 'docviewer-' + docviewer_index);
							var id = $(this).attr('id');
							docviewer_index++;
						} else {
							var id = $(this).attr('id');
						}
            docviewer.load('/documents/doc-'+$(this).attr('data-document')+'.json', {
									container : '#'+id,
									sidebar : false
								});
					});
		});
