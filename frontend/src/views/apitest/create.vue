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
              <el-form-item label-width="120px" label="项目名称:" style="width:500px;">
                <el-select
                @change="getProjectSetting"
                v-model="postForm.project_id"
                placeholder="请选择项目"
                value-key="id">
                  <el-option v-for="(item, index)  in projectSelect"
                  :label="item.project_name"
                  :value="index"
                  :key="item.id">
                  </el-option>
                </el-select>
              </el-form-item>
              <el-row>
                <el-col :span="16">
                <el-form-item label-width="120px" label="请求地址:">
                  <el-input placeholder="输入请求地址" v-model="postForm.uri"></el-input>
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
                <el-input type="textarea"  :rows="3" placeholder="请输入请求头" v-model="postForm.headers" style="width:500px;">
                </el-input>
              </el-form-item>
              <el-form-item label-width="120px" label="请求体:">
                <el-input type="textarea"  :rows="3" placeholder="请输入请求body" v-model="postForm.params" style="width:500px;">
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
                     v-model="postForm.token_user"
                     filterable
                     remote
                     reserve-keyword
                     placeholder="用户关键词"
                     :remote-method="getRemoteUserList">
                     <el-option
                       v-for="item in userLIstOptions"
                       :key="item.key"
                       :label="item.name"
                       :value="item.key">
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
                  <el-input placeholder="套件名即为unittest测试类名" v-model="postForm.suite_name"></el-input>
                </el-form-item>
                </el-col>
                <el-col :span="8">
                <el-form-item label-width="120px" label="用例方法名:">
                  <el-input placeholder="unittest测试方法名" v-model="postForm.func_name"></el-input>
                </el-form-item>
                </el-col>
              </el-row>
              <el-form-item label-width="700px">
                <el-button type="primary" @click="createApiTestCase">立即创建</el-button>
                <el-button>取消</el-button>
              </el-form-item>
            </el-form>
          </div>
        </el-card>
      </el-col>

      <el-col :span="10" hidden>
        <el-card class="box-card">
          <div slot="header" class="clearfix">
            <span>图片hover效果</span>
          </div>
          <div class="component-item">
            <pan-thumb width="100px" height="100px" image="https://wpimg.wallstcn.com/577965b9-bb9e-4e02-9f0c-095b41417191">
              vue-element-admin
            </pan-thumb>
          </div>
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
import { apiTokenUserSearch, testCaseAdd } from '@/api/apitest'
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
  token_user: '',
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
    this.getProjectList()
  },
  data() {
    return {
      postForm: Object.assign({}, defaultForm),
      projects: '',
      reqeustMethod: [
        { key: 1, name: 'GET' },
        { key: 2, name: 'POST' },
        { key: 3, name: 'PUT' },
        { key: 4, name: 'DELETE' }
      ],
      projectSelect: '',
      userLIstOptions: [],
      listQuery: {
        search: ''
      },
      caseRules: {
        uri: [{ required: true }]
      }
    }
  },
  methods: {
    getProjectSetting: function(index, key) {
      const apiSttings = this.projectSelect[index]
      apiSttings.setting.map(v => {
        if (v.setting_type === 0) {
          this.postForm.uri = v.setting_value
        } else if (v.setting_type === 1) {
          this.postForm.headers = v.setting_value
        } else if (v.setting_type === 2) {
          this.postForm.params = v.setting_value
        }
      })
    },
    getProjectList() {
      projectList(this.listQuery).then(response => {
        if (!response.data) return
        this.projectSelect = response.data.data
        console.log(this.projectSelect)
      })
    },
    getRemoteUserList(search) {
      apiTokenUserSearch(search).then(response => {
        if (!response.data.results) return
        console.log(response)
        this.userLIstOptions = response.data.results.map(v => ({
          key: v.id,
          name: v.username
        }))
      })
    },
    createApiTestCase() {
      testCaseAdd(this.postForm).then(response => {
        if (response.data) {
          this.$router.go(0)
        }
      })
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
