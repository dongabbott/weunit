<template>
  <div class="app-container calendar-list-container">
    <div class="filter-container">
      <el-input @keyup.enter.native="handleFilter" style="width: 200px;" class="filter-item" placeholder="用户名或描述" v-model="listQuery.search">
      </el-input>
      <el-button class="filter-item" type="primary" v-waves icon="el-icon-search" @click="handleFilter">搜索</el-button>
      <el-button class="filter-item" style="margin-left: 10px;" @click="handleCreate" type="primary" icon="el-icon-edit">添加</el-button>
      <el-button class="filter-item" type="primary" v-waves icon="el-icon-download" @click="handleDownload">导出</el-button>
    </div>

    <el-table :key='tableKey' :data="list" v-loading="listLoading" element-loading-text="给我一点时间" border fit highlight-current-row
      style="width: 100%">
      <el-table-column align="center" label="序号" width="65">
        <template slot-scope="scope">
          <span>{{scope.row.id}}</span>
        </template>
      </el-table-column>
      <el-table-column min-width="200px" label="帐号描述">
        <template slot-scope="scope">
          <span>{{scope.row.user_desc}}</span>
        </template>
      </el-table-column>
      <el-table-column width="300px" align="left" label="帐号信息">
        <template slot-scope="scope">
          <li>{{scope.row.username}}</li>
          <li>{{scope.row.password}}</li>
        </template>
      </el-table-column>
      <el-table-column class-name="status-col" label="token值" width="200">
        <template slot-scope="scope">
          <span>{{scope.row.token_value}}</span>
        </template>
      </el-table-column>
      <el-table-column class-name="status-col" label="token有效期" width="80">
        <template slot-scope="scope">
          <span>{{scope.row.token_term}}</span>
        </template>
      </el-table-column>
      <el-table-column class-name="status-col" label="更新时间" width="200">
        <template slot-scope="scope">
          <span>{{scope.row.update_time}}</span>
        </template>
      </el-table-column>
      <el-table-column align="center" label="操作" width="350" class-name="small-padding">
        <template slot-scope="scope">
          <el-button type="primary" size="mini" @click="testUserUpdate(scope.row)">编辑</el-button>
          </el-button>
          <el-button type="info" size="mini" @click="refreshUserToken(scope.row)">刷新token</el-button>
          </el-button>
          <el-button size="mini" type="danger" @click="deleteTestUser(scope.row.id)">删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <div v-show="!listLoading" class="pagination-container">
      <el-pagination background  @current-change="handleCurrentChange" :current-page.sync="listQuery.page"
        :page-sizes="[10]" :page-size="10" layout="total, sizes, prev, pager, next, jumper" :total="total">
      </el-pagination>
    </div>

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible">
      <el-form :rules="rules" ref="dataForm" :model="temp" label-position="left" label-width="70px" style='width: 400px; margin-left:50px;'>
        <el-form-item  label-width="120px" label="帐号简述" prop="user_desc">
          <el-input v-model="temp.user_desc"></el-input>
        </el-form-item>
        <el-form-item label-width="120px" label="项目名称:" style="width:500px;">
          <el-select
            v-model="temp.project_id"
            filterable
            allow-create
            default-first-option
            placeholder="请选择项目">
            <el-option
              v-for="item in projectSelect"
              :key="item.key"
              :label="item.name"
              :value="item.key">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label-width="120px" label="用户名" prop="username">
          <el-input v-model="temp.username" placeholder="example: username=13476085026"></el-input>
        </el-form-item>
        <el-form-item label-width="120px" label="密码" prop="password">
          <el-input v-model="temp.password" placeholder="example: password=123456"></el-input>
        </el-form-item>
        <el-form-item label-width="120px" label="token有效期">
          <el-input v-model="temp.token_term"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button v-if="dialogStatus=='create'" type="primary" @click="createTestuser">确 定</el-button>
        <el-button v-else type="primary" @click="updateData(temp.id)">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { apiTokenUsersList, testUserAdd, apiTestUserUpdate, apiTestUserDelete, apiTokenRefresh } from '@/api/apitest'
import waves from '@/directive/waves' // 水波纹指令
import { parseTime } from '@/utils'
import { projectList } from '@/api/project'

export default {
  name: 'projectTable',
  directives: {
    waves
  },
  data() {
    return {
      tableKey: 0,
      list: null,
      total: null,
      listLoading: true,
      projectSelect: [],
      listQuery: {
        search: null
      },
      sortOptions: [{ label: '按ID升序列', key: '+id' }, { label: '按ID降序', key: '-id' }],
      statusOptions: ['published', 'draft', 'deleted'],
      showAuditor: false,
      temp: {
        id: undefined,
        username: '',
        password: '',
        user_desc: '',
        project_id: null,
        token_term: ''
      },
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: '编辑',
        create: '创建'
      },
      dialogPvVisible: false,
      rules: {
        username: [{ required: true, message: '用户名必须', trigger: 'blur' }],
        password: [{ required: true, message: '密码必须', trigger: 'blur' }],
        user_desc: [{ required: true, message: '描述必须', trigger: 'blur' }]
      }
    }
  },
  filters: {
    statusFilter(status) {
      const statusMap = {
        published: 'success',
        draft: 'info',
        deleted: 'danger'
      }
      return statusMap[status]
    }
  },
  created() {
    this.getList()
    this.getProjectList()
  },
  methods: {
    getProjectList() {
      projectList(this.listQuery).then(response => {
        if (!response.data) return
        this.projectSelect = response.data.results.map(v => ({
          key: v.id,
          name: v.project_name
        }))
        console.log(this.projectSelect)
      })
    },
    getList() {
      this.listLoading = true
      apiTokenUsersList(this.listQuery).then(response => {
        this.list = response.data.results
        this.total = response.data.count
        this.listLoading = false
      })
    },
    testUserUpdate(row) {
      this.temp = Object.assign({}, row) // copy obj
      this.dialogStatus = 'update'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    createTestuser() {
      this.$refs.dataForm.validate(valid => {
        if (valid) {
          testUserAdd(this.temp).then(response => {
            if (response.data) {
              this.$router.go(0)
            }
          })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    refreshUserToken(row) {
      apiTokenRefresh(row.id).then(response => {
        console.log(response.data)
      })
    },
    deleteTestUser(row) {
      apiTestUserDelete(row).then(response => {
        this.$notify({
          title: '成功',
          message: '删除成功',
          type: 'success',
          duration: 2000
        })
        const index = this.list.indexOf(row)
        this.list.splice(index, 1)
      })
    },
    updateData(id) {
      apiTestUserUpdate(id, this.temp).then(response => {
        if (response.data.id) {
          this.$router.go(0)
        }
      })
    },
    handleFilter() {
      this.listQuery.page = 1
      this.getList()
    },
    handleSizeChange(val) {
      this.listQuery.limit = val
      this.getList()
    },
    handleCurrentChange(val) {
      this.listQuery.page = val
      this.getList()
    },
    resetTemp() {
      this.temp = {
        id: undefined,
        username: '',
        password: '',
        user_desc: '',
        project_id: null,
        token_term: ''
      }
    },
    handleCreate() {
      this.resetTemp()
      console.log(this.resetTemp())
      this.dialogStatus = 'create'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    handleUpdate(row) {
      this.temp = Object.assign({}, row) // copy obj
      this.temp.timestamp = new Date(this.temp.timestamp)
      this.dialogStatus = 'update'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    handleDownload() {
      require.ensure([], () => {
        const { export_json_to_excel } = require('vendor/Export2Excel')
        const tHeader = ['时间', '地区', '类型', '标题', '重要性']
        const filterVal = ['timestamp', 'province', 'type', 'title', 'importance']
        const data = this.formatJson(filterVal, this.list)
        export_json_to_excel(tHeader, data, 'table数据')
      })
    },
    formatJson(filterVal, jsonData) {
      return jsonData.map(v => filterVal.map(j => {
        if (j === 'timestamp') {
          return parseTime(v[j])
        } else {
          return v[j]
        }
      }))
    }
  }
}
</script>
