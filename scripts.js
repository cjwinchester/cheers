var phrase = 'CHEERS';

var phrase_count = phrase.split('').reduce(function(prev, item) { 
  if (item in prev) {
    prev[item]++;
  } else {
    prev[item] = 1;
  };
  return prev; 
}, {});

var napkin = document.getElementById('napkin');
var button = document.getElementsByTagName('button')[0];
var combo = document.getElementById('combo-count');

// https://stackoverflow.com/a/2450976
function shuffle(array) {
  let currentIndex = array.length, randomIndex;
  while (currentIndex != 0) {
    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex--;
    [array[currentIndex], array[randomIndex]] = [
      array[randomIndex], array[currentIndex]];
  }
  return array;
}

var xhr = new XMLHttpRequest();
xhr.open('GET', 'cheers.json', true);
xhr.onload = function (e) {
  if (xhr.readyState === 4) {
    if (xhr.status === 200) {
      var resp = JSON.parse(xhr.responseText);
      var data = resp['data'];
      var count = resp['possible_combinations'];
      combo.innerHTML = 'at least ' + count;
      button.innerHTML = 'New napkin';
      button.disabled = false;

      var keys = Object.keys(data);

      function getNewCities() {
        // https://stackoverflow.com/a/15106541
        var random_idx = keys[keys.length * Math.random() << 0];
        var idx_list = data[random_idx];

        var table_data = {
          'idx': parseInt(random_idx),
          'words': []
        };

        for (letter in phrase_count) {
          var letter_count = phrase_count[letter];
          var city_list = idx_list[letter];
          shuffle(city_list);
          var cities = city_list.slice(0, letter_count);
          cities.forEach(function(x) {
            table_data['words'].push(x)
          });
        }
        return table_data;        
      };

      function makeNewNapkin() {
        var city_data = getNewCities();
        var cities = city_data['words'];
        var table_idx = city_data['idx'];
        var napkin_html = '';
        
        for (var i=0; i<cities.length; i++) {
          var city = cities[i];
          var this_graf = '<p>';
          for (var z=0; z<city.length; z++) {
            var letter = city[z];
            if (z === table_idx) {
              this_graf += '<span class="highlight">' + letter + '</span>';
            } else {
              this_graf += letter;
            }
          }
          this_graf += '</p>';
          napkin_html += this_graf;
        };
        napkin.innerHTML = napkin_html;
      };

      button.addEventListener('click', makeNewNapkin, false);

      button.click();

    } else {
      console.error(xhr.statusText);
    }
  }
};
xhr.onerror = function (e) {
  console.error(xhr.statusText);
};
xhr.send(null);