import request from '@/utils/request'

export function loginByUsername(username, password) {
  const data = {
    username,
    password
  }
  return request({
    url: '/api/account/login',
    method: 'post',
    data
  })
}

export function logout() {
  return request({
    url: '/api/account/logout',
    method: 'post'
  })
}

export function getUserInfo(token) {
  return request({
    url: '/api/account/userinfo/',
    method: 'get'
  })
}
