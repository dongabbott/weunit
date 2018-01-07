<template>
  <div class="app-container calendar-list-container">
    <div class="filter-container">
      <el-input @keyup.enter.native="handleFilter" style="width: 200px;" class="filter-item" placeholder="项目名" v-model="listQuery.project_name">
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
      <el-table-column width="180px" align="center" label="项目名称">
        <template slot-scope="scope">
          <span>{{scope.row.project_name}}</span>
        </template>
      </el-table-column>
      <el-table-column min-width="200px" label="项止描述">
        <template slot-scope="scope">
          <span>{{scope.row.project_desc}}</span>
        </template>
      </el-table-column>
      <el-table-column class-name="status-col" label="状态" width="100">
        <template slot-scope="scope">
          <el-tag v-if="scope.row.project_status == true" type="success">启用</el-tag>
          <el-tag v-if="scope.row.project_status == false" type="danger">关闭</el-tag>
        </template>
      </el-table-column>
      <el-table-column class-name="status-col" label="项目key" width="200">
        <template slot-scope="scope">
          <span>{{scope.row.project_key}}</span>
        </template>
      </el-table-column>
      <el-table-column class-name="status-col" label="创建时间" width="200">
        <template slot-scope="scope">
          <span>{{scope.row.create_time}}</span>
        </template>
      </el-table-column>
      <el-table-column align="center" label="操作" width="350" class-name="small-padding">
        <template slot-scope="scope">
          <el-button type="primary" size="mini" @click="userUpdate(scope.row)">编辑</el-button>
          </el-button>
          <el-button  size="mini" type="info" @click="userGroupHandle(scope.row)">项目配置
          </el-button>
          <el-button size="mini" type="danger" @click="deletePorject(scope.row.id)">删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <div v-show="!listLoading" class="pagination-container">
      <el-pagination background @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page.sync="listQuery.page"
        :page-sizes="[10,20,30, 50]" :page-size="listQuery.limit" layout="total, sizes, prev, pager, next, jumper" :total="total">
      </el-pagination>
    </div>

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible">
      <el-form :rules="rules" ref="dataForm" :model="temp" label-position="left" label-width="70px" style='width: 400px; margin-left:50px;'>
        <el-form-item label="用例名称">
          <el-input v-model="temp.name"></el-input>
        </el-form-item>
        <el-form-item label="unitest套件名">
          <el-input type="textarea" v-model="temp.project_desc"></el-input>
        </el-form-item>
        <el-form-item label="unitest">
          <el-input type="textarea" v-model="temp.project_desc"></el-input>
        </el-form-item>
        <el-form-item label="状态">
          <input type="radio" v-model="temp.project_status" v-bind:value="true"><label>启用</label>
          <input type="radio" v-model="temp.project_status" v-bind:value="false"><label>禁用</label>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button v-if="dialogStatus=='create'" type="primary" @click="createPorject">确 定</el-button>
        <el-button v-else type="primary" @click="updateData(temp.id)">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { projectList, projectAdd, projectDel, projectEdit } from '@/api/project'
import waves from '@/directive/waves' // 水波纹指令
import { parseTime } from '@/utils'

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
      listQuery: {
        page: 1,
        project_name: null,
        project_desc: null,
        project_status: true,
        limit: 20
      },
      selectGroupKeyValue: null,
      sortOptions: [{ label: '按ID升序列', key: '+id' }, { label: '按ID降序', key: '-id' }],
      statusOptions: ['published', 'draft', 'deleted'],
      showAuditor: false,
      temp: {
        id: undefined,
        name: '',
        uri: '',
        suite_name: '',
        func_name: '',
        method: '',
        is_token: '',
        reqeust_after: '',
        request_befor: '',
        request_body: '',
        request_headers: ''
      },
      dialogFormVisible: false,
      dialogGroup: false,
      dialogStatus: '',
      textMap: {
        update: '编辑',
        create: '创建'
      },
      dialogPvVisible: false,
      rules: {
        project_name: [{ type: 'date', required: true, message: 'timestamp is required', trigger: 'change' }],
        project_desc: [{ required: true, message: 'title is required', trigger: 'blur' }]
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
  },
  methods: {
    getList() {
      this.listLoading = true
      projectList(this.listQuery).then(response => {
        this.list = response.data.data
        this.total = response.data.count
        this.listLoading = false
      })
    },
    userUpdate(row) {
      this.temp = Object.assign({}, row) // copy obj
      this.dialogStatus = 'update'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    createPorject() {
      projectAdd(this.temp).then(response => {
        if (response.data) {
          this.$router.go(0)
        }
      })
    },
    deletePorject(row) {
      projectDel(row).then(response => {
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
      console.log(this.temp)
      projectEdit(id, this.temp).then(response => {
        if (response.data.id) {
          this.$router.go(0)
        }
      })
    },
    userGroupHandle(row) {
      this.dialogStatus = 'setting'
      this.dialogGroup = true
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
        project_name: '',
        project_desc: '',
        project_status: true
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
