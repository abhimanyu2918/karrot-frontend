<template>
  <div>
    <q-card>
      <div
        class="edit-box"
        :class="{ changed: hasChanged }"
      >
        <form @submit.prevent="maybeSave">
          <q-field
            v-if="!edit.isPlayground"
            icon="fas fa-fw fa-star"
            :label="$t('GROUP.TITLE')"
            :error="hasNameError"
            :error-label="nameError"
          >
            <q-input
              id="group-title"
              v-model="edit.name"
              :autofocus="true"
              autocomplete="off"
              @blur="$v.edit.name.$touch"
            />
          </q-field>

          <q-field
            v-if="!edit.isPlayground"
            icon="fas fa-fw fa-question"
            :label="$t('GROUP.PUBLIC_DESCRIPTION')"
            :error="hasError('publicDescription')"
            :error-label="firstError('publicDescription')"
          >
            <MarkdownInput :value="edit.publicDescription">
              <q-input
                v-model="edit.publicDescription"
                type="textarea"
                rows="3"
                @keyup.ctrl.enter="maybeSave"
                style="min-height: 5em"
              />
            </MarkdownInput>
          </q-field>

          <q-field
            icon="fas fa-fw fa-address-card"
            :label="$t('GROUP.DESCRIPTION_VERBOSE')"
            :error="hasError('description')"
            :error-label="firstError('description')"
          >
            <MarkdownInput :value="edit.description">
              <q-input
                v-model="edit.description"
                type="textarea"
                rows="3"
                @keyup.ctrl.enter="maybeSave"
                style="min-height: 5em"
              />
            </MarkdownInput>
          </q-field>

          <q-field
            icon="fas fa-fw fa-map-marker"
            :label="$t('GROUP.ADDRESS')"
            :error="hasAddressError"
            :error-label="addressError"
          >
            <AddressPicker
              v-model="edit"
              :color="isNew ? 'blue' : 'positive'"
              font-icon="fas fa-home"
            />
          </q-field>

          <q-field
            v-if="!edit.isPlayground"
            icon="fas fa-fw fa-question"
            :label="$t('GROUP.PASSWORD')"
            :error="hasError('password')"
            :error-label="firstError('password')"
          >
            <q-input v-model="edit.password"/>
          </q-field>

          <q-field
            icon="fas fa-fw fa-globe"
            :label="$t('GROUP.TIMEZONE')"
            :error="hasTimezoneError"
            :error-label="timezoneError"
          >
            <q-input
              v-model="edit.timezone"
              @blur="$v.edit.timezone.$touch"
            >
              <q-autocomplete
                :static-data="timezones"
                :max-results="10"
                :debounce="300"
                :filter="timezoneFilter"
              />
            </q-input>
          </q-field>

          <div
            v-if="hasNonFieldError"
            class="text-negative"
          >
            {{ firstNonFieldError }}
          </div>
          <div class="actionButtons">
            <q-btn
              type="button"
              @click="reset"
              v-if="!isNew"
              :disable="!hasChanged"
            >
              {{ $t('BUTTON.RESET') }}
            </q-btn>

            <q-btn
              type="submit"
              color="primary"
              :disable="!canSave"
              :loading="isPending"
            >
              {{ $t(isNew ? 'BUTTON.CREATE' : 'BUTTON.SAVE_CHANGES') }}
            </q-btn>
          </div>
        </form>
      </div>
    </q-card>
  </div>
</template>

<script>
import jstz from 'jstimezonedetect'
import { QCard, QField, QInput, QBtn, QAutocomplete } from 'quasar'
import StandardMap from '@/components/Map/StandardMap'
import AddressPicker from '@/components/Address/AddressPicker'
import MarkdownInput from '@/components/MarkdownInput'
import { validationMixin } from 'vuelidate'
import { required, minLength, maxLength } from 'vuelidate/lib/validators'
import editMixin from '@/mixins/editMixin'
import statusMixin from '@/mixins/statusMixin'

export default {
  name: 'GroupEdit',
  mixins: [validationMixin, editMixin, statusMixin],
  props: {
    value: {
      type: Object,
      required: false,
      default: () => ({
        name: undefined,
        password: undefined,
        publicDescription: undefined,
        description: undefined,
        timezone: jstz.determine().name(),
        latitude: undefined,
        longitude: undefined,
        address: undefined,
      }),
    },
    timezones: {
      type: Object,
      required: true,
    },
    allGroups: {
      type: Array,
      required: true,
    },
  },
  components: {
    QCard, QField, QInput, QBtn, QAutocomplete, StandardMap, AddressPicker, MarkdownInput,
  },
  computed: {
    canSave () {
      if (this.$v.edit.$error) {
        return false
      }
      if (!this.isNew && !this.hasChanged) {
        return false
      }
      return true
    },
    hasNameError () {
      return !!this.nameError
    },
    nameError () {
      if (this.$v.edit.name.$error) {
        const m = this.$v.edit.name
        if (!m.required) return this.$t('VALIDATION.REQUIRED')
        if (!m.minLength) return this.$t('VALIDATION.MINLENGTH', {min: 4})
        if (!m.maxLength) return this.$t('VALIDATION.MAXLENGTH', {max: 81})
        if (!m.isUnique) return this.$t('VALIDATION.UNIQUE')
      }
      return this.firstError('name')
    },
    hasTimezoneError () {
      return !!this.timezoneError
    },
    timezoneError () {
      if (this.$v.edit.timezone.$error) {
        const m = this.$v.edit.timezone
        if (!m.required) return this.$t('VALIDATION.REQUIRED')
        if (!m.inList) return this.$t('VALIDATION.VALID_TIMEZONE')
      }
      return this.firstError('timezone')
    },
    hasAddressError () {
      return !!this.addressError
    },
    addressError () {
      for (let field of ['address', 'latitude', 'longitude']) {
        if (this.hasError(field)) return this.firstError(field)
      }
    },
  },
  methods: {
    maybeSave (event) {
      this.$v.edit.$touch()
      if (!this.canSave) return
      this.$v.edit.$reset()
      this.save()
    },
    timezoneFilter (terms, { field, list }) {
      const token = terms.toLowerCase()
      return list.filter(item => item[field].toLowerCase().includes(token))
    },
  },
  validations: {
    edit: {
      name: {
        required,
        minLength: minLength(5),
        maxLength: maxLength(80),
        isUnique (value) {
          if (value === '' || !this.value) return true
          return this.allGroups
            .filter(e => e.id !== this.value.id)
            .findIndex(e => e.name === value) < 0
        },
      },
      timezone: {
        required,
        inList (value) {
          if (value === '') return true
          if (this.timezones && this.timezones.list) {
            return this.timezones.list.findIndex(e => e.value === value) > 0
          }
          return true
        },
      },
    },
  },
}
</script>

<style scoped lang="stylus">
@import '~editbox'
</style>
