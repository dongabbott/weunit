import request from '@/utils/request'

// 用户列表接口读取
export function accountList(query) {
  return request({
    url: '/api/account/users/',
    method: 'get',
    params: query
  })
}

// 用户添加接口
export function accountAdd(data) {
  return request({
    url: '/api/account/users/',
    method: 'post',
    data
  })
}

// 用户组接口读取
export function groupList() {
  return request({
    url: '/api/account/groups/',
    method: 'get'
  })
}

// 用户删除接口
export function accountDelete(id) {
  return request({
    url: '/api/account/users/' + id + '/',
    method: 'delete'
  })
}

// 用户更新
export function accountUpdate(id, data) {
  return request({
    url: '/api/account/users/' + id + '/',
    method: 'put',
    data
  })
}
