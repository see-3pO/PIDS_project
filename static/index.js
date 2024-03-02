
//digital clock
function getDateTime() {
    // Get current date and time
    const date = new Date();

    // Extract date components
    const year = date.getFullYear();
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const day = date.getDate().toString().padStart(2, '0');

    // Extract time components
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');
    const seconds = date.getSeconds().toString().padStart(2, '0');

    // Format date and time using template literals
    const dateString = `${year}-${month}-${day}`;
    const timeString = `${hours}:${minutes}:${seconds}`;

    // Display date and time in HTML
    document.getElementById("date").textContent = dateString;
    document.getElementById("time").textContent = timeString;
}

getDateTime();

setInterval(getDateTime, 1000);

function updateData() {
  fetch('/get_latest_data')
      .then(response => response.json())
      .then(data => {
          document.getElementById('duration').innerText = data.duration;
          document.getElementById('nextStop').innerText = data.next_stop;

          //getting the timeline items
          const timelineItems = document.querySelectorAll('.timeline-item');

          //loop through each timeline item
          timelineItems.forEach(item=>
          {
              const stopName = item.dataset.stopName;
              //check if stop name matches the next stop name
              if (stopName == data.next_stop){
                  //adding a class to that timeline item for styling
                  item.classList.add('active-stop');
              }else{
                  //remove the class if the stop name doesn't match
                  item.classList.remove('active-stop');
              }
          });
      })
      .catch(error => console.error('Error fetching data:', error));
}

setInterval(updateData, 60000);




// Test code

$('.progress').each((_, progress) => {
  
  const steps = $('> div.right > div', progress);

  steps.each((i, el) => $(el).mouseenter(e => onHover(el)));

  const onHover = (el) => {
      steps.removeClass(['current', 'prev']);
      el.classList.add('current');
      $(el).prevAll().slice(1).addClass('prev');
    };
})

