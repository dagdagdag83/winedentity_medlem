function onSubmit(token) {
  document.querySelector('form').submit();
}

document.addEventListener('DOMContentLoaded', function() {
  flatpickr("#birth_date", {
    dateFormat: "d/m/Y",
  });

  const countrySelect = document.querySelector('#country');
  const countries = JSON.parse(countrySelect.dataset.countries || '[]');

  new TomSelect("#country",{
    maxOptions: null,
    options: countries,
    valueField: 'value',
    labelField: 'text',
    searchField: 'text',
    render: {
      option: function(data, escape) {
        if (data.value === 'XX') {
          return '<div>' + escape(data.text) + '</div>';
        }
        return '<div><span class="flag-icon flag-icon-' + escape(data.value.toLowerCase()) + ' mr-2"></span>' + escape(data.text) + '</div>';
      },
      item: function(data, escape) {
        if (data.value === 'XX') {
          return '<div>' + escape(data.text) + '</div>';
        }
        return '<div><span class="flag-icon flag-icon-' + escape(data.value.toLowerCase()) + ' mr-2"></span>' + escape(data.text) + '</div>';
      }
    }
  });
});
