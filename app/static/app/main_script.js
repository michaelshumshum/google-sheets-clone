window.addEventListener('DOMContentLoaded', addAllEventListeners)

function addAllEventListeners() {
  document.querySelectorAll('.tab-group').forEach(element => {
    i = sessionStorage.getItem(`${window.location.pathname}-${element.id}`)
    if (i) {
      element.childNodes[i].classList.add('active')
    } else {
      element.childNodes[1].classList.add('active')
    }
  })
  document.querySelectorAll('.tab-content-group').forEach(element => {
    i = sessionStorage.getItem(`${window.location.pathname}-${element.parentElement.id}`)
    if (i) {
      element.childNodes[i].classList.add('active')
    } else {
      element.childNodes[1].classList.add('active')
    }
  })
  document.querySelector('#raw-data-btn').addEventListener('click', redirectToRaw)
  document.querySelector('#back-btn').addEventListener('click', redirectBack)
  document.querySelector('#reset-btn').addEventListener('click', resetParams)
  document.querySelector('#apply-btn').addEventListener('click', submitForm)
  document.querySelectorAll('input').forEach(element => {
    element.addEventListener('input', submitFormOnChange)
  })
  document.querySelectorAll('select').forEach(element => {
    element.addEventListener('input', submitFormOnChange)
  })
  document.querySelectorAll('.tab-group').forEach(element => {
    element.addEventListener('click', tabSwitch)
  })
  if (sessionStorage.getItem(`${window.location.pathname}-autoapply`)) {
    document.querySelector('#auto-apply').checked = sessionStorage.getItem(`${window.location.pathname}-autoapply`)
  }
  window.addEventListener('beforeunload', function(event) {
    sessionStorage.setItem(`${window.location.pathname}-autoapply`, document.querySelector('#auto-apply').checked)
  })
}

function redirectToRaw() {
  window.open(window.location.href.split('?')[0] + 'raw', '_blank')
}

function redirectBack() {
  window.location.replace(window.location.origin)
}

function resetParams() {
  window.location.replace(window.location.href.split('?')[0])
}

function submitForm() {
  document.querySelector('#controller-form').submit()
}

function submitFormOnChange(event) {
  if (document.querySelector('#auto-apply').checked && event.target.parentElement.tagname == 'FORM') {
    submitForm()
  }
}

function tabSwitch(event) {
  if (!event.target.classList.contains('tab-btn')) {
    return
  }
  if (event.target.classList.contains('active')) {
    return
  }
  parent = event.target.parentElement
  parent.querySelector('.tab-btn.active').classList.remove('active')
  parent.querySelector('.tab-content-group').querySelector('.tab-content.active').classList.remove('active')
  event.target.classList.add('active')
  sessionStorage.setItem(`${window.location.pathname}-${parent.id}`, Array.from(parent.childNodes).indexOf(event.target))
  parent.querySelector(`.tab-content.${event.target.classList[1]}`).classList.add('active')
}