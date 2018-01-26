<template>
  <div class="mixin-components-container">
    <el-row :gutter="20" style="margin-top:50px;">
      <el-col :span="14">
        <el-card class="box-card">
          <div slot="header" class="clearfix">
            <span>创建接口用例</span>
          </div>
          <div class="component-item" style="height:autosize;">
            <el-form :model="postForm" :rules="caseRules">
              <el-form-item label-width="120px" label="项目名称:" style="width:500px;" >
                <el-select
                 v-model="postForm.project_id"
                 filterable
                 remote
                 reserve-keyword
                 placeholder="项目"
                 :remote-method="getProjectList"
                 @change="getProjectSetting"
                 value-key="id">
                 <el-option
                   v-for="(item, index) in projectSelect"
                   :key="item.id"
                   :label="item.project_name"
                   :value="item.id">
                 </el-option>
               </el-select>
              </el-form-item>
              <el-row>
                <el-col :span="16">
                  <el-form-item label-width="120px" label="请求地址:">
                    <el-input  v-model="postForm.uri" v-bind:placeholder="$t(this.address)"></el-input>
                  </el-form-item>
                </el-col>
                <el-col :span="3">
                <el-form-item>
                  <el-select
                  v-model="postForm.method"
                  placeholder="请求方式">
                    <el-option v-for="(item, index)  in reqeustMethod"
                    :label="item.name"
                    :value="item.key"
                    :key="item.id">
                    </el-option>
                  </el-select>
                </el-form-item>
                </el-col>
              </el-row>
              <el-form-item label-width="120px" label="请求头:">
                <el-input type="textarea"  :rows="3" placeholder="http headers" v-model="postForm.headers" style="width:500px;">
                </el-input>
              </el-form-item>
              <el-form-item label-width="120px" label="请求体:">
                <el-input type="textarea"  :rows="3" placeholder="http reqeust body" v-model="postForm.params" style="width:500px;">
                </el-input>
              </el-form-item>
              <el-row>
                <el-col :span="9">
                  <el-form-item label-width="120px" label="是否登录:">
                    <el-switch
                      v-model="postForm.is_token"
                      active-color="#13ce66"
                      inactive-color="#ff4949">
                    </el-switch>
                  </el-form-item>
                </el-col>
                <el-col :span="8" v-if="postForm.is_token===true" v-show="true">
                  <el-form-item label-width="120px" label="登录用户:">
                    <el-select
                     v-model="postForm.token_user_id"
                     filterable
                     remote
                     reserve-keyword
                     placeholder="测试用户"
                     :remote-method="getRemoteUserList"
                     value-key="id">
                     <el-option
                       v-for="item in userLIstOptions"
                       :key="item.id"
                       :label="item.user_desc"
                       :value="item.id">
                     </el-option>
                   </el-select>
                  </el-form-item>
                </el-col>
              </el-row>
              <el-form-item label-width="120px" label="用例名称:" style="width:500px;">
                <el-input placeholder="输入用例名称" v-model="postForm.name"></el-input>
              </el-form-item>
              <el-row>
                <el-col :span="9">
                <el-form-item label-width="120px" label="前置条件:">
                  <el-input placeholder="example:" v-model="postForm.c_before"></el-input>
                </el-form-item>
                </el-col>
                <el-col :span="9">
                <el-form-item label-width="120px" label="后置条件:">
                  <el-input placeholder="example:" v-model="postForm.c_after"></el-input>
                </el-form-item>
                </el-col>
              </el-row>
              <el-form-item label-width="120px" label="用例描述:">
                <el-input type="textarea"  :rows="3" placeholder="请输入请求body" v-model="postForm.description" style="width:500px;">
                </el-input>
              </el-form-item>
              <el-row>
                <el-col :span="9">
                <el-form-item label-width="120px" label="套件名称:">
                  <el-select v-model="postForm.suite_name" placeholder="请选择">
                    <el-option
                      v-for="item in testSuiteOptions"
                      :key="item.value"
                      :label="item.label"
                      :value="item.value">
                    </el-option>
                  </el-select>
                </el-form-item>
                </el-col>
                <el-col :span="8">
                <el-form-item label-width="120px" label="用例方法名:">
                  <el-input placeholder="unittest测试方法名" v-model="postForm.func_name"></el-input>
                </el-form-item>
                </el-col>
              </el-row>
              <el-form-item label-width="700px">
                <el-button type="primary" @click="createApiTestCase">立即{{this.button[this.action]}}</el-button>
                <el-button type="primary" @click="apiDebug">调试</el-button>
              </el-form-item>
            </el-form>
          </div>
        </el-card>
      </el-col>

      <el-col :span="10" v-show="debugCard">
        <el-card class="box-card">
          <el-tabs v-model="activeName">
            <el-tab-pane v-bind:label="$t(this.status)" name="body">
              <div v-if="this.jsonSource.type ==='json'">
                <tree-view
                :data="this.jsonSource.content"
                :options="{rootObjectKey: 'data'}">
                </tree-view>
              </div>
              <div v-else>
                {{this.jsonSource.content}}
              </div>
            </el-tab-pane>
            <el-tab-pane v-bind:label="$t(this.times)" name="headers">
              <div>
                <tree-view
                :data="this.showHeaders"
                :options="{rootObjectKey: 'data'}">
                </tree-view>
              </div>
            </el-tab-pane>
            <el-tab-pane label="请求信息" name="req">
              <div>
                <li>请求地址：{{this.postForm.uri}}</li>
                <li>请求头：{{this.postForm.headers}}</li>
                <li>请求参数： {{this.postForm.params}}</li>
              </div>
            </el-tab-pane>
          </el-tabs>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import PanThumb from '@/components/PanThumb'
import MdInput from '@/components/MDinput'
import Mallki from '@/components/TextHoverEffect/Mallki'
import DropdownMenu from '@/components/Share/dropdownMenu'
import waves from '@/directive/waves/index.js' // 水波纹指令
import Tinymce from '@/components/Tinymce'
import Upload from '@/components/Upload/singleImage3'
import Multiselect from 'vue-multiselect'
import { apiTokenUserSearch, testCaseAdd, apiTestDetail, testCaseUpdate, apiDebug } from '@/api/apitest'
import { projectList } from '@/api/project'

const defaultForm = {
  name: '',
  suite_name: '',
  func_name: '',
  method: '',
  uri: '',
  headers: '',
  params: '',
  is_token: false,
  token_user_id: null,
  c_after: '',
  c_before: '',
  project_id: null,
  description: ''
}
export default {
  name: 'componentMixin-demo',
  components: {
    PanThumb,
    MdInput,
    Mallki,
    DropdownMenu,
    Multiselect,
    Tinymce,
    Upload
  },
  directives: {
    waves
  },
  created() {
    if (this.$route.params.id) {
      this.action = 'update'
      apiTestDetail(this.$route.params.id).then(response => {
        if (response.data) {
          this.postForm = response.data
        }
      })
    }
    this.getProjectList()
    this.getRemoteUserList()
  },
  data() {
    return {
      postForm: Object.assign({}, defaultForm),
      action: 'create',
      button: {
        create: '创建',
        update: '更新'
      },
      address: '',
      reqeustMethod: [],
      projectSelect: '',
      userLIstOptions: [],
      testSuiteOptions: [],
      debugCard: false,
      activeName: 'body',
      jsonSource: '',
      status: '',
      times: '',
      showHeaders: '',
      listQuery: {
        search: ''
      },
      reqResult: null,
      caseRules: {
        uri: [{ required: true }]
      }
    }
  },
  methods: {
    getProjectSetting: function(index) {
      alert(index)
      const chose_project = this.projectSelect[index]
      console.log(chose_project)
      this.projectSelect.map(v => {
        if (v.id === index) {
          const apiSttings = v
          apiSttings.setting.map(v => {
            if (v.setting_type === 0) {
              this.address = v.setting_value
            } else if (v.setting_type === 1) {
              this.postForm.headers = v.setting_value
            } else if (v.setting_type === 2) {
              this.postForm.params = v.setting_value
            }
          })
        }
      })
    },
    getProjectList() {
      projectList(this.listQuery).then(response => {
        if (!response.data) return
        this.projectSelect = response.data.results
        this.reqeustMethod = response.data.reqeust_method
        if (this.postForm.project_id !== '') {
          const project = this.projectSelect.filter(v => v.id === this.postForm.project_id)
          const setting = project[0].setting.filter(v => v.setting_type === 0)[0].setting_value
          this.address = setting
        }
      })
    },
    getRemoteUserList(search) {
      apiTokenUserSearch(search).then(response => {
        if (!response.data.results) return
        this.userLIstOptions = response.data.results
      })
    },
    createApiTestCase() {
      if (this.action === 'create') {
        testCaseAdd(this.postForm).then(response => {
          if (response.data) {
            this.$router.push({ path: '/apitest/index' })
          }
        })
      } else if (this.action === 'update') {
        testCaseUpdate(this.$route.params.id, this.postForm).then(response => {
          if (response.data) {
            this.$router.push({ path: '/apitest/index' })
          }
        })
      }
    },
    apiDebug() {
      const url = this.address + '/' + this.postForm.uri
      const data = {
        url: url,
        params: this.postForm.params,
        headers: this.postForm.headers,
        method: this.postForm.method,
        project_id: this.postForm.project_id,
        user_id: this.postForm.token_user_id
      }
      apiDebug(data).then(response => {
        this.debugCard = true
        this.jsonSource = response.data.data.body
        this.status = '响应数据' + '[' + response.data.data.status + ']'
        this.times = '响应头' + '[' + response.data.data.time + '-ms]'
        this.showHeaders = response.data.data.headers
      })
    },
    onChangeData: function(data) {
      console.log(JSON.stringify(data))
    },
    showCreatedTimes() {
      this.createdTimes = this.createdTimes + 1
    }
  }
}
</script>

<style scoped>
.mixin-components-container {
  background-color: #f0f2f5;
  padding: 30px;
  min-height: calc(100vh - 84px);
}
.component-item{
  min-height: 100px;
}
</style>
