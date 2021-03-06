<template>
  <div v-if="group">
    <q-card class="shadow-6">
      <q-card-title
        :class="group.isPlayground ? 'text-secondary' : ''"
      >
        <span class="row group items-start">
          {{ group.name }}
          <q-icon
            v-if="group.isPlayground"
            name="fas fa-child"
            color="secondary"
          />
        </span>
        <span slot="subtitle">
          {{ group.members.length }} {{ $tc('JOINGROUP.NUM_MEMBERS', group.members.length) }}
        </span>
        <q-btn
          v-if="showClose"
          slot="right"
          round
          small
          @click="$emit('close')"
          color="primary"
          class="preview-close-button"
        >
          <q-icon name="fas fa-times" />
          <q-tooltip>
            {{ $t('BUTTON.CLOSE') }}
          </q-tooltip>
        </q-btn>
      </q-card-title>
      <q-card-main>
        <div
          v-if="group.publicDescription"
          class="quote"
        >
          <Markdown :source="group.publicDescription" />
        </div>
        <span
          v-else
          class="text-italic"
        >
          {{ $t('JOINGROUP.NO_PUBLIC_DESCRIPTION') }}
        </span>
      </q-card-main>
      <q-card-separator />
      <q-card-actions>
        <span
          v-if="!group.isMember"
          style="width: 100%">
          <form
            name="joingroup"
            @submit.prevent="$emit('join', { groupId: group.id, password })"
          >
            <q-alert
              v-if="!group.isMember"
              color="warning"
              icon="info"
            >
              {{ $t('JOINGROUP.PROFILE_NOTE' ) }}
            </q-alert>
            <q-field
              v-if="group.protected"
              icon="fas fa-lock"
              :label="$t('JOINGROUP.PASSWORD_REQUIRED')"
              :helper="$t('JOINGROUP.PASSWORD_LABEL')"
              :error="hasAnyError"
              :error-label="anyFirstError"
            >
              <q-input
                v-model="password"
                type="password"
              />
            </q-field>
            <q-btn
              type="submit"
              color="secondary"
              class="float-right generic-margin"
              :loading="group.joinStatus.pending"
            >
              {{ $t( isLoggedIn ? 'BUTTON.JOIN' : 'JOINGROUP.SIGNUP_OR_LOGIN') }}
            </q-btn>
          </form>
        </span>
        <q-btn
          v-if="group.isMember"
          @click="$emit('visit', { groupId: group.id })"
          class="q-btn-flat"
        >
          <q-icon name="fas fa-home" />
          <q-tooltip>
            {{ $t('GROUPINFO.MEMBER_VIEW') }}
          </q-tooltip>
        </q-btn>
      </q-card-actions>
    </q-card>
  </div>
</template>

<script>
import { QCard, QCardTitle, QCardMain, QCardSeparator, QCardActions, QBtn, QField, QInput, QIcon, QTooltip, QAlert } from 'quasar'
import Markdown from '@/components/Markdown'

export default {
  data () {
    return { password: '' }
  },
  props: {
    group: {
      default: null,
      type: Object,
    },
    isLoggedIn: {
      default: false,
      type: Boolean,
    },
    showClose: {
      default: false,
      type: Boolean,
    },
  },
  components: { QCard, QCardTitle, QCardMain, QCardSeparator, QCardActions, QBtn, QField, QInput, QIcon, QTooltip, QAlert, Markdown },
  computed: {
    joinStatus () {
      return this.group && this.group.joinStatus
    },
    hasAnyError () {
      return this.joinStatus && this.joinStatus.hasValidationErrors
    },
    anyFirstError () {
      return this.joinStatus && this.joinStatus.firstValidationError
    },
  },
}
</script>

<style scoped lang="stylus">
.q-card *
  overflow: hidden
</style>
