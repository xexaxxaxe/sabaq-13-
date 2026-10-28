// Предварительный расчёт цены в форме бронирования.
// Сама цена считается на сервере (/api/quote), здесь её только показываем.
(function () {
  const form = document.getElementById("booking-form");
  if (!form) return;

  const box = document.getElementById("quote");
  const button = document.getElementById("book-button");
  const WEEKDAYS = ["вс", "пн", "вт", "ср", "чт", "пт", "сб"];
  let lastRequest = 0;

  function money(value) {
    return value.toLocaleString("ru-RU").replace(/[\u00a0\u202f]/g, " ") + " ₸";
  }

  function dayLabel(iso) {
    const [y, m, d] = iso.split("-").map(Number);
    const day = new Date(y, m - 1, d);   // местная дата, без часовых поясов
    return `${WEEKDAYS[day.getDay()]} ${String(d).padStart(2, "0")}.${String(m).padStart(2, "0")}`;
  }

  function render(data) {
    if (data.error) {
      const p = document.createElement("p");
      p.className = "error";
      p.textContent = data.error;   // текст ошибки содержит то, что ввёл пользователь
      box.replaceChildren(p);
      button.disabled = true;
      return;
    }
    const rows = data.nights
      .map((n) => `<tr><td>ночь с ${dayLabel(n.day)}${n.weekend ? " · выходная" : ""}</td><td>${money(n.price)}</td></tr>`)
      .join("");
    let extra = `<tr class="quote__sum"><td>Итого за ночи</td><td>${money(data.subtotal)}</td></tr>`;
    if (data.long_stay_percent) {
      extra += `<tr><td>Скидка за долгое проживание</td><td>−${data.long_stay_percent} %</td></tr>`;
    }
    if (data.promo_percent) {
      extra += `<tr><td>Промокод ${data.promo_code}</td><td>−${data.promo_percent} %</td></tr>`;
    }
    extra += `<tr class="quote__total"><td>К оплате</td><td>${money(data.total)}</td></tr>`;
    const busy = data.free ? "" : `<p class="error">На эти даты номер занят</p>`;
    box.innerHTML = `<table>${rows}${extra}</table>${busy}`;
    button.disabled = !data.free;
  }

  async function update() {
    const params = new URLSearchParams({
      room: form.dataset.room,
      check_in: form.check_in.value,
      check_out: form.check_out.value,
      guests: form.guests.value,
      promo: form.promo.value,
    });
    const requestId = ++lastRequest;
    try {
      const response = await fetch("/api/quote?" + params.toString());
      const data = await response.json();
      if (requestId === lastRequest) render(data);   // показываем только самый свежий ответ
    } catch (e) {
      box.innerHTML = `<p class="error">Нет связи с сервером</p>`;
    }
  }

  form.addEventListener("input", update);
  update();
})();
