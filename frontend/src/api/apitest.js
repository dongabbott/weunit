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

// 刷新token
export function apiTokenRefresh(id) {
  return request({
    url: '/api/apitest/users/refresh/',
    method: 'post',
    data: { user_id: id }
  })
}

export function testSuiteList(query) {
  return request({
    url: '/api/apitest/suite/',
    method: 'get',
    params: query
  })
}

// 套件添加接口
export function testSuiteAdd(data) {
  return request({
    url: '/api/apitest/suite/',
    method: 'post',
    data
  })
}

// 套件更新
export function testSuiteUpdate(id, data) {
  return request({
    url: '/api/apitest/suite/' + id + '/',
    method: 'put',
    data
  })
}

// 套件删除接口
export function testSuiteDelete(id) {
  return request({
    url: '/api/apitest/suite/' + id + '/',
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

// 用例更新
export function testCaseUpdate(id, data) {
  return request({
    url: '/api/apitest/case/' + id + '/',
    method: 'put',
    data
  })
}

// 用例删除接口
export function apiTestCaseDelete(id) {
  return request({
    url: '/api/apitest/case/' + id + '/',
    method: 'delete'
  })
}

// 用例列表数据
export function apiTestCaseList(query) {
  return request({
    url: '/api/apitest/case/',
    method: 'get',
    params: query
  })
}

// 用例查询
export function apiTestSearch(query) {
  return request({
    url: '/api/apitest/case/',
    method: 'get',
    params: query
  })
}

export function apiTestDetail(id) {
  return request({
    url: '/api/apitest/case/' + id + '/',
    method: 'get'
  })
}

// api请求接口调试
export function apiDebug(data) {
  return request({
    url: '/api/apitest/case/debug/',
    method: 'post',
    data
  })
}
