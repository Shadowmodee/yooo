//VIEW MORE BUTTONS

if ($('.box-hidden').length > 2) {
  $('.box-hidden:gt(1)').hide();
  $('.load0').show();
}

$('.load0').on('click', function() {
  //toggle elements with class .ty-compact-list that their index is bigger than 2
  $('.box-hidden:gt(1)').toggle();
  //change text of show more element just for demonstration purposes to this demo
  $(this).text() === 'Show more' ? $(this).text('Show less') : $(this).text('Show more');
});


if ($('.box-hidden1').length > 2) {
  $('.box-hidden1:gt(1)').hide();
  $('.load1').show();
}

$('.load1').on('click', function() {
  //toggle elements with class .ty-compact-list that their index is bigger than 2
  $('.box-hidden1:gt(1)').toggle();
  //change text of show more element just for demonstration purposes to this demo
  $(this).text() === 'Show more' ? $(this).text('Show less') : $(this).text('Show more');
});

if ($('.box-hidden2').length > 2) {
  $('.box-hidden2:gt(1)').hide();
  $('.load2').show();
}

$('.load2').on('click', function() {
  //toggle elements with class .ty-compact-list that their index is bigger than 2
  $('.box-hidden2:gt(1)').toggle();
  //change text of show more element just for demonstration purposes to this demo
  $(this).text() === 'Show more' ? $(this).text('Show less') : $(this).text('Show more');
});


if ($('.box-hidden3').length > 2) {
  $('.box-hidden3:gt(1)').hide();
  $('.load3').show();
}

$('.load3').on('click', function() {
  //toggle elements with class .ty-compact-list that their index is bigger than 2
  $('.box-hidden3:gt(1)').toggle();
  //change text of show more element just for demonstration purposes to this demo
  $(this).text() === 'Show more' ? $(this).text('Show less') : $(this).text('Show more');
});

if ($('.box-hidden4').length > 2) {
  $('.box-hidden4:gt(1)').hide();
  $('.load4').show();
}

$('.load4').on('click', function() {
  //toggle elements with class .ty-compact-list that their index is bigger than 2
  $('.box-hidden4:gt(1)').toggle();
  //change text of show more element just for demonstration purposes to this demo
  $(this).text() === 'Show more' ? $(this).text('Show less') : $(this).text('Show more');
});

if ($('.box-hidden5').length > 2) {
  $('.box-hidden5:gt(1)').hide();
  $('.load5').show();
}

$('.load5').on('click', function() {
  //toggle elements with class .ty-compact-list that their index is bigger than 2
  $('.box-hidden5:gt(1)').toggle();
  //change text of show more element just for demonstration purposes to this demo
  $(this).text() === 'Show more' ? $(this).text('Show less') : $(this).text('Show more');
});

if ($('.box-hidden6').length > 2) {
  $('.box-hidden6:gt(1)').hide();
  $('.load6').show();
}

$('.load6').on('click', function() {
  //toggle elements with class .ty-compact-list that their index is bigger than 2
  $('.box-hidden6:gt(1)').toggle();
  //change text of show more element just for demonstration purposes to this demo
  $(this).text() === 'Show more' ? $(this).text('Show less') : $(this).text('Show more');
});


$(function() {
  $(document).on('click', '#checkAll', function() {
  
      if ($(this).val() == 'Uncheck All') {
		$('.button input').prop('checked', false);
		$(this).val('Check All');
      } else {
		$('.button input').prop('checked', true);
		$(this).val('Uncheck All');
      }
  });
});


/*$( document ).ready(function () {
    $(".box-hidden").slice(0, 1).show();
      if ($(".box-hidden:hidden").length != 0) {
        $("#load0").show();
      }   
      $("#load0").on('click', function (e) {
        e.preventDefault();
        $(".box-hidden:hidden").slice(0,).slideDown();
        if ($(".box-hidden:hidden").length == 0) {
          $("#load0").fadeOut('slow');
        }
      });
});

$( document ).ready(function () {
    $(".box-hidden1").slice(0, 1).show();
      if ($(".box-hidden1:hidden").length != 0) {
        $("#load1").show();
      }   
      $("#load1").on('click', function (e) {
        e.preventDefault();
        $(".box-hidden1:hidden").slice(0,).slideDown();
        if ($(".box-hidden1:hidden").length == 0) {
          $("#load1").fadeOut('slow');
        }
      });
});

$( document ).ready(function () {
    $(".box-hidden2").slice(0, 1).show();
      if ($(".box-hidden2:hidden").length != 0) {
        $("#load2").show();
      }   
      $("#load2").on('click', function (e) {
        e.preventDefault();
        $(".box-hidden2:hidden").slice(0,).slideDown();
        if ($(".box-hidden2:hidden").length == 0) {
          $("#load2").fadeOut('slow');
        }
      });
});

$( document ).ready(function () {
    $(".box-hidden3").slice(0, 1).show();
      if ($(".box-hidden3:hidden").length != 0) {
        $("#load3").show();
      }   
      $("#load3").on('click', function (e) {
        e.preventDefault();
        $(".box-hidden3:hidden").slice(0,).slideDown();
        if ($(".box-hidden3:hidden").length == 0) {
          $("#load3").fadeOut('slow');
        }
      });
});

$( document ).ready(function () {
    $(".box-hidden4").slice(0, 1).show();
      if ($(".box-hidden4:hidden").length != 0) {
        $("#load4").show();
      }   
      $("#load4").on('click', function (e) {
        e.preventDefault();
        $(".box-hidden4:hidden").slice(0,).slideDown();
        if ($(".box-hidden4:hidden").length == 0) {
          $("#load4").fadeOut('slow');
        }
      });
});

$( document ).ready(function () {
    $(".box-hidden5").slice(0, 1).show();
      if ($(".box-hidden5:hidden").length != 0) {
        $("#load5").show();
      }   
      $("#load5").on('click', function (e) {
        e.preventDefault();
        $(".box-hidden5:hidden").slice(0,).slideDown();
        if ($(".box-hidden5:hidden").length == 0) {
          $("#load5").fadeOut('slow');
        }
      });
});

$( document ).ready(function () {
    $(".box-hidden6").slice(0, 1).show();
      if ($(".box-hidden6:hidden").length != 0) {
        $("#load6").show();
      }   
      $("#load6").on('click', function (e) {
        e.preventDefault();
        $(".box-hidden6:hidden").slice(0,).slideDown();
        if ($(".box-hidden6:hidden").length == 0) {
          $("#load6").fadeOut('slow');
        }
      });
});*/

//this will execute on page load(to be more specific when document ready event occurs)


// TEXT OVER IMAGE
    /*dragElement(document.getElementById("exampleModal"));

    function dragElement(elmnt) {
    var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
    if (document.getElementById(elmnt.id + "header")) {
        // if present, the header is where you move the DIV from:
        document.getElementById(elmnt.id + "header").onmousedown = dragMouseDown;
    } else {
        // otherwise, move the DIV from anywhere inside the DIV:
        elmnt.onmousedown = dragMouseDown;
    }

    function dragMouseDown(e) {
        e = e || window.event;
        e.preventDefault();
        // get the mouse cursor position at startup:
        pos3 = e.clientX;
        pos4 = e.clientY;
        document.onmouseup = closeDragElement;
        // call a function whenever the cursor moves:
        document.onmousemove = elementDrag;
    }

    function elementDrag(e) {
        e = e || window.event;
        e.preventDefault();
        // calculate the new cursor position:
        pos1 = pos3 - e.clientX;
        pos2 = pos4 - e.clientY;
        pos3 = e.clientX;
        pos4 = e.clientY;
        // set the element's new position:
        elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
        elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
    }

    function closeDragElement() {
        // stop moving when mouse button is released:
        document.onmouseup = null;
        document.onmousemove = null;
    }
    }*/
