import request from '@/utils/request'

// 读取测试用户列表数据
export function apiTokenUsersList(query) {
  return request({
    url: '/api/apitest/users/',
    method: 'get',
    params: query
  })
}

// 用户查询
export function apiTokenUserSearch(query) {
  return request({
    url: '/api/apitest/users/',
    method: 'get',
    params: { search: query }
  })
}

// 用户添加接口
export function testUserAdd(data) {
  return request({
    url: '/api/apitest/users/',
    method: 'post',
    data
  })
}

// 用户更新
export function apiTestUserUpdate(id, data) {
  return request({
    url: '/api/apitest/users/' + id + '/',
    method: 'put',
    data
  })
}

// 用户删除接口
export function apiTestUserDelete(id) {
  return request({
    url: '/api/apitest/users/' + id + '/',
    method: 'delete'
  })
}

// 用例创建
export function testCaseAdd(data) {
  return request({
    url: '/api/apitest/case/',
    method: 'post',
    data
  })
}
