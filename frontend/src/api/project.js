import request from '@/utils/request'

// 读取所有项目
export function projectList(query) {
  return request({
    url: '/api/project/',
    method: 'get',
    params: query
  })
}

// 项目添加
export function projectAdd(data) {
  return request({
    url: '/api/project/',
    method: 'post',
    data
  })
}

// 项目删除
export function projectDel(id) {
  return request({
    url: '/api/project/' + id + '/',
    method: 'delete'
  })
}

// 项目编辑
export function projectEdit(id, data) {
  return request({
    url: '/api/project/' + id + '/',
    method: 'put',
    data
  })
}
