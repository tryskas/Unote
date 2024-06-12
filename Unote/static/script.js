window.onload = function() {
    $(document.body).addClass("no-transition");
    $(".theme-switch").addClass("no-transition");
    $(".sun").addClass("no-transition");

    var theme = localStorage.getItem('theme');
    switch (theme) {
        case 'dark-theme':
            $(document.body).toggleClass("dark-theme");
            $(".theme-switch").toggleClass('day');
            $(".sun").toggleClass('moon');
            break;
        default:
            localStorage.setItem("theme","light-theme")
    }

    setTimeout(function () {
        $(document.body).removeClass("no-transition");
        $(".theme-switch").removeClass("no-transition");
        $(".sun").removeClass("no-transition");
    }, 1);
}

$(document).ready(function() {
    $(".theme-switch").click(function() {
        var theme = localStorage.getItem('theme');
        $(document.body).toggleClass("dark-theme");
        $(".theme-switch").toggleClass('day');
        $(".sun").toggleClass('moon');
        switch (theme) {
            case 'dark-theme':
                localStorage.setItem("theme","light-theme")
                break;
            case 'light-theme':
                localStorage.setItem("theme","dark-theme")
                break;
        }
    });
});