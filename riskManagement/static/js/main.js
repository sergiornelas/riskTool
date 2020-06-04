const date = new Date();
document.querySelector('.year').innerHTML = date.getFullYear();

setTimeout(function() {
    $('#message').fadeOut('slow');
}, 3000);


$("div[id^='myModal']").each(function(){
  
    var currentModal = $(this);
    
    //click next
    currentModal.find('.btn-next').click(function(){
      currentModal.modal('hide');
      currentModal.closest("div[id^='myModal']").nextAll("div[id^='myModal']").first().modal('show'); 
    });
    
    //click prev
    currentModal.find('.btn-prev').click(function(){
      currentModal.modal('hide');
      currentModal.closest("div[id^='myModal']").prevAll("div[id^='myModal']").first().modal('show'); 
    });
  
  });
  