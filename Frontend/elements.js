document.addEventListener("DOMContentLoaded", function () {
  var $bar = $(".progress .bar");
  var $val = $(".progress #rating");

  // Function to update the progress bar based on the rating value
  function updateProgressBar() {
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
                      borderRightColor: color,
                      borderBottomColor: color,
                  });
                  $val.text((p / 20).toFixed(1));
              },
          }
      );
  }

  // Function to get a color based on the percentage value
  function getColorForPercentage(percentage) {
      var hue = (percentage / 100) * 120;
      return "hsl(" + hue + ", 100%, 50%)";
  }

  // Initial setup
  updateProgressBar();

  // Listen for the custom "ratingUpdated" event
  document.getElementById("rating").addEventListener("ratingUpdated", function () {
      updateProgressBar();
  });
});
