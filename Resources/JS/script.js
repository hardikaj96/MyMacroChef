$(document).ready(function() {

	// For the sticky navigation
    $('.js--section-features').waypoint(function(direction) {
        if(direction == "down") {
            $('nav').addClass('sticky');
        } else {
            $('nav').removeClass('sticky');
        }
    }, {
        offset: '60px;'
    });

    // Scroll on buttons 
    $('.js--scroll-to-plans').click(function () {
        $('html, body').animate({scrollTop: $('.js--section-plans').offset().top}, 1000); 
     });
     
     $('.js--scroll-to-start').click(function () {
        $('html, body').animate({scrollTop: $('.js--section-features').offset().top}, 1000); 
     });

    // Navigation scroll

    // Select all links with hashes
    $('a[href*="#"]')
    // Remove links that don't actually link to anything
    .not('[href="#"]')
    .not('[href="#0"]')
    .click(function(event) {
    // On-page links
    if (
        location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') 
        && 
        location.hostname == this.hostname
    ) {
        // Figure out element to scroll to
        var target = $(this.hash);
        target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
        // Does a scroll target exist?
        if (target.length) {
        // Only prevent default if animation is actually gonna happen
        event.preventDefault();
        $('html, body').animate({
            scrollTop: target.offset().top
        }, 1000, function() {
            // Callback after animation
            // Must change focus!
            var $target = $(target);
            $target.focus();
            if ($target.is(":focus")) { // Checking if the target was focused
            return false;
            } else {
            $target.attr('tabindex','-1'); // Adding tabindex for elements not focusable
            $target.focus(); // Set focus again
            };
        });
        }
    }
    });

    // Animation on scroll
    $('.js--wp-1').waypoint(function(direction) {
        $('.js--wp-1').addClass('animated fadeIn');
    }, {
        offset: '50%'
    });
    
    $('.js--wp-2').waypoint(function(direction) {
        $('.js--wp-2').addClass('animated fadeInUp');
    }, {
        offset: '50%'
    });
    
    $('.js--wp-3').waypoint(function(direction) {
        $('.js--wp-3').addClass('animated fadeIn');
    }, {
        offset: '50%'
    });
    
    $('.js--wp-4').waypoint(function(direction) {
        $('.js--wp-4').addClass('animated pulse');
    }, {
        offset: '50%'
    });

    // Mobile navigation
    $('.js--nav-icon').click(function() {
        var nav = $('.js--main-nav');
        var icon = $('.js--nav-icon i');
        
        nav.slideToggle(200);
        
        if (icon.hasClass('ion-navicon-round')) {
            icon.addClass('ion-close-round');
            icon.removeClass('ion-navicon-round');
        } else {
            icon.addClass('ion-navicon-round');
            icon.removeClass('ion-close-round');
        }        
    });
	
	//Plan
	var value = $( '#planselect').val();
	var bill="";
	var msg="";
	var price="";
	if(value=="monthly_plan") {
		msg = "Saving $250 a month";
		price = "$800"+"/month + tax".sub();
		bill = "$"+(800+(800*10/100));
	} else if(value=="weekly_plan") {
		msg = "Saving $45 a week";
		price = "$200"+"/week + tax".sub();
		bill = "$"+(200+(200*10/100));
	} else {
		msg = "Must try, you won't regret it!";
		price = "$35"+"/day + tax".sub();
		bill = "$"+(35+(35*10/100));
	}
	if (document.getElementById("plan-msg")) {
		document.getElementById("plan-msg").innerHTML = msg;
		document.getElementById("plan-price").innerHTML = price;
		document.getElementById("total-bill").innerHTML = bill;
	}
	
	$('select').on('change', function() {
	  alert( $('option:selected', this).attr('KCal') );
	});
	
});

var headerValue;
function setPrefRecom(buttonValue){
	headerValue=buttonValue;
}
function getPrefRecom(){
	if(headerValue="recom"){
		document.getElementById("pref_recom").innerHTML="Recommendations";
		document.getElementById("sub_update").disabled=true;
	} else {
		document.getElementById("pref_recom").innerHTML="My Preferences";
		document.getElementById("sub_recom").disabled=true;
	}
}

function addDiv(ev) {
	console.log(ev);
}