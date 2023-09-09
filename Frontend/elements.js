$(document).ready(function () {
  // Your jQuery code here
  $(".progress").each(function () {
      var $bar = $(this).find(".bar");
      var $val = $(this).find("#rating");
      var rating = parseFloat($val.text());
      var perc = (rating / 5) * 100;

      $({ p: 0 }).animate(
          { p: perc },
          {
              duration: 3000,
              easing: "swing",
              step: function (p) {
                  // Calculate the color based on the percentage
                  var color = getColorForPercentage(p);
                  $bar.css({
                      transform: "rotate(" + (45 + p * 1.8) + "deg)",
                      borderRightColor: color, // Change border color
                      borderBottomColor: color // Change border color
                  });
                  $val.text((p / 20).toFixed(1)); // Convert percentage to rating value
              }
          }
      );
  });

  // Function to get a color based on the percentage value
  function getColorForPercentage(percentage) {
      var hue = (percentage / 100) * 120; // 0% = red, 100% = green (HSL color model)
      return "hsl(" + hue + ", 100%, 50%)";
  }
});