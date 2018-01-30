<template>
  <div class="app-container calendar-list-container">
    <div class="filter-container">
      <el-select clearable class="filter-item" style="width: 130px" v-model="listQuery.project_id" placeholder="所属项目">
        <el-option v-for="item in projectSelect" :key="item.key" :label="item.name" :value="item.key">
        </el-option>
      </el-select>
      <el-input @keyup.enter.native="handleFilter" style="width: 200px;" class="filter-item" placeholder="套件名称" v-model="listQuery.suite_name">
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
      <el-table-column min-width="200px" label="套件名称">
        <template slot-scope="scope">
          <span>{{scope.row.suite_name}}</span>
        </template>
      </el-table-column>
      <el-table-column width="300px" align="left" label="套件描述">
        <template slot-scope="scope">
          <span>{{scope.row.suite_desc}}</span>
        </template>
      </el-table-column>
      <el-table-column width="80px" align="left" label="用例个数">
        <template slot-scope="scope">
          <span>{{scope.row.case_count}}</span>
        </template>
      </el-table-column>
      <el-table-column class-name="status-col" label="更新时间" width="200">
        <template slot-scope="scope">
          <span>{{scope.row.create_time}}</span>
        </template>
      </el-table-column>
      <el-table-column align="center" label="操作" width="350" class-name="small-padding">
        <template slot-scope="scope">
          <el-button type="primary" size="mini" @click="testSuiteUpdate(scope.row)">编辑</el-button>
          </el-button>
          <el-button type="waring" size="mini">生成unit</el-button>
          </el-button>
          <el-button type="info" size="mini" @click="editTestUnitCase(scope.row)">编辑unit</el-button>
          </el-button>
          <el-button size="mini" type="danger" @click="deleteTestSuite(scope.row.id)">删除
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
        <el-form-item label-width="120px" label="套件名" prop="suite_name">
          <el-input v-model="temp.suite_name" placeholder="example: TestUserLoginCase"></el-input>
        </el-form-item>
        <el-form-item label-width="120px" label="套件描述">
          <el-input v-model="temp.suite_desc"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button v-if="dialogStatus=='create'" type="primary" @click="createTestSuite">确 定</el-button>
        <el-button v-else type="primary" @click="updateData(temp.id)">确 定</el-button>
      </div>
    </el-dialog>

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="codingFormVisible" :model="temp">
        <codemirror ref="myCm"
              :value="this.unit_code"
              :options="cmOptions"
              @input="onCmCodeChange">
        </codemirror>
    <div slot="footer" class="dialog-footer">
      <el-button @click="codingFormVisible = false">取 消</el-button>
      <el-button type="primary" @click="SaveCodingFile(temp)">确 定</el-button>
    </div>
    </el-dialog>
  </div>
</template>

<script>
import { testSuiteList, testSuiteAdd, testSuiteDelete, getCoding, saveCoding } from '@/api/apitest'
import waves from '@/directive/waves' // 水波纹指令
import { parseTime } from '@/utils'
import { projectList } from '@/api/project'
import { codemirror } from 'vue-codemirror'
import 'codemirror/lib/codemirror.css'
// language
import 'codemirror/mode/python/python.js'
// theme css
import 'codemirror/theme/base16-light.css'
// require active-line.js
import 'codemirror/addon/selection/active-line.js'
// closebrackets
import 'codemirror/addon/edit/closebrackets.js'
// keyMap
import 'codemirror/mode/clike/clike.js'
import 'codemirror/addon/edit/matchbrackets.js'
import 'codemirror/addon/comment/comment.js'
import 'codemirror/addon/dialog/dialog.js'
import 'codemirror/addon/dialog/dialog.css'
import 'codemirror/addon/search/searchcursor.js'
import 'codemirror/addon/search/search.js'
import 'codemirror/keymap/emacs.js'

export default {
  name: 'projectTable',
  directives: {
    waves
  },
  components: {
    codemirror
  },
  computed: {
    codemirror() {
      return this.$refs.myCm.codemirror
    }
  },
  data() {
    return {
      tableKey: 0,
      list: null,
      total: null,
      listLoading: true,
      projectSelect: [],
      listQuery: {
        project_id: null,
        suite_name: null
      },
      temp: {
        id: undefined,
        suite_name: '',
        suite_desc: '',
        project_id: null
      },
      unit_code: '',
      dialogFormVisible: false,
      codingFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: '编辑',
        create: '创建',
        coding: '代码编辑'
      },
      dialogPvVisible: false,
      cmOptions: {
        // codemirror options
        autoCloseBrackets: true,
        tabSize: 4,
        styleActiveLine: true,
        lineNumbers: true,
        line: true,
        mode: 'text/x-python',
        theme: 'base16-light',
        keyMap: 'emacs'
      },
      rules: {
        suite_name: [{ required: true, message: '套件名必须填写', trigger: 'blur' }]
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
      testSuiteList(this.listQuery).then(response => {
        this.list = response.data.results
        this.total = response.data.count
        this.listLoading = false
      })
    },
    testSuiteUpdate(row) {
      this.temp = Object.assign({}, row) // copy obj
      this.dialogStatus = 'update'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    createTestSuite() {
      this.$refs.dataForm.validate(valid => {
        if (valid) {
          testSuiteAdd(this.temp).then(response => {
            if (response.data) {
              this.getList()
              this.dialogFormVisible = false
            }
          })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    deleteTestSuite(row) {
      testSuiteDelete(row).then(response => {
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
    SaveCodingFile(row) {
      const data = {
        active: 'save',
        coding: this.unit_code
      }
      saveCoding(row.id, data).then(response => {
        if (response.data) {
          console.log(response.data)
        }
      })
    },
    editTestUnitCase(row) {
      this.temp = Object.assign({}, row)
      this.dialogStatus = 'coding'
      this.codingFormVisible = true
      getCoding(row.id).then(response => {
        if (response.data.last === null) {
          this.unit_code = response.data.file_content
        } else {
          this.unit_code = response.data.last
        }
      })
    },
    editTestCaseHandle(row) {
      this.$router.push({ path: '/apitest/edit/' + row.id })
    },
    onCmCodeChange(newCode) {
      this.unit_code = newCode
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
        suite_name: '',
        suite_desc: '',
        project_id: null
      }
    },
    handleCreate() {
      this.resetTemp()
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
