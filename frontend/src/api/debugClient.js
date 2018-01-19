import axios from 'axios'
import qs from 'qs'

function toType(obj) {
  return ({}).toString.call(obj).match(/\s([a-zA-Z]+)/)[1].toLowerCase()
}

function filterNull(o) {
  for (var key in o) {
    if (o[key] === null) {
      delete o[key]
    }
    if (toType(o[key]) === 'string') {
      o[key] = o[key].trim()
    } else if (toType(o[key]) === 'object') {
      o[key] = filterNull(o[key])
    } else if (toType(o[key]) === 'array') {
      o[key] = filterNull(o[key])
    }
  }
  return o
}

export function apiAxios(host, uri, method, params, token) {
  if (params) {
    params = qs.stringify(filterNull(params))
  }
  axios({
    method: method,
    url: uri,
    data: method === 'POST' || method === 'PUT' ? params : null,
    params: method === 'GET' || method === 'DELETE' ? params : null,
    baseURL: host,
    withCredentials: true,
    headers: {
      'Access-Control-Allow-Origin': host
    }
  })
    .then(res => {
      return Promise.reject(res)
    })
    .catch(function(error) {
      if (error.response) return
      else {
        console.log('Error', error.message)
      }
      console.log(error.config)
    })
}
