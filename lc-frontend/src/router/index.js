import {createRouter, createWebHistory} from 'vue-router'
import Explore from '@/views/explore-page.vue'
import MainPage from '@/views/main-page.vue'
import FounderSpace from '@/views/founder-space/secret.vue'
import FounderSpaceEdit from '@/views/founder-space/edit.vue'
import FounderSpaceDecisions from '@/views/founder-space/decisions.vue'
import FounderSpaceChat from '@/views/founder-space/chat.vue'
import JobPage from '@/views/job-view/view.vue'
import FounderSpaceSettings from '@/views/founder-space/settings.vue'
import Login from '@/views/user-create/login.vue'
import createUser from '@/views/user-create/create.vue'
import Success from '@/views/user-create/success.vue'
import UserView from '@/views/user-create/user-view.vue'
import UserSettings from '@/views/user-create/user-settings.vue'
import UserProjects from '@/views/user-create/user-projects.vue'
import Notifications from "@/views/user-create/notifications.vue"
import Chatrooms from "@/views/user-create/chatrooms.vue"
import FounderSpacePeople from "@/views/founder-space/people.vue"
import userApplications from '@/views/user-create/user-applications.vue'
import Friends from '@/views/user-create/friends.vue'
import callback from '@/views/user-create/callback.vue'
import Verify from '@/views/user-create/verify.vue'
import passwordReset from '@/views/user-create/password-reset.vue'
import ProjectCreate from '@/views/project-create/projectCreate.vue'
import ProjectView from '@/views/project_view/project.vue'
const routes = [
    {
        path: '/',
        component: MainPage
    },
    {
        path: '/password-reset',
        component: passwordReset
    },
    {
        path: '/project/:projectId',
        component: ProjectView
    },
    {
        path: '/project-create',
        component: ProjectCreate
    },
    {
        path: '/verify',
        component: Verify
    },
    {
        path: '/auth/callback',
        component: callback
    },
    {
        path: '/friends/:usertag',
        component: Friends
    },
    {
        path: '/applications',
        component: userApplications
    },
    {
        path: '/notifications',
        component: Notifications
    },
    {
        path: '/messages',
        component: Chatrooms
    },
    {
        path: '/user-projects/:usertag',
        component: UserProjects
    },
    {
        path: '/explore',
        component: Explore
    },
    {
        path: '/login',
        component: Login
    },
    {
        path: '/account-setup',
        component: createUser
    },
    {
        path: '/success',
        component: Success
    },
    {
        path: '/profile/:usertag',
        component: UserView
    },
    {
        path: '/settings',
        component: UserSettings
    },
    {
        path: '/project-edit/:projectId',
        component: FounderSpace
    },
    {
        path: '/project-edit/:projectId/edit',
        component: FounderSpaceEdit
    },
    {
        path: '/project-edit/:projectId/votes/:tab',
        component: FounderSpaceDecisions
    },
    {
        path: '/project-edit/:projectId/chat',
        component: FounderSpaceChat
    },
    {
        path: '/project-edit/:projectId/settings',
        component: FounderSpaceSettings
    },
    {
        path: '/project-edit/:projectId/people',
        component: FounderSpacePeople
    },
    {
        path: '/job',
        component: JobPage
    }
    
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router