var options = [
    {selector: '#staggered-test', offset: 400, callback: function(el) {
      Materialize.showStaggeredList($(el));
    } }
  ];
  Materialize.scrollFire(options);

  $(document).ready(function() {
    $('select').material_select();
    $('.modal').modal();

    $('.alert-close').on('click', function(c){
		$(this).parent().parent().parent().parent().fadeOut('slow', function(c){
		});
	});	
  });
  
           