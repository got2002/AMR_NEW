<template>
    <button
        class="w-10 h-10 bg-white shadow-sm rounded-md text-base border flex items-center justify-center"
        :class="buttonClasses"
        :disabled="disabled"
        :title="title"
        @click="pageChange"
    >
        <i
            v-if="loading"
            class="fa fa-spinner fa-spin"
        />
        <span
            v-else
            v-html="html"
        />
    </button>
</template>

<script>
export default {
    name: 'VueAdsPageButton',

    props: {
        page: {
            type: [
                Number,
                String,
            ],
            required: true,
        },

        active: {
            type: Boolean,
            default: false,
        },

        disabled: {
            type: Boolean,
            default: false,
        },

        html: {
            type: String,
            required: true,
        },

        title: {
            type: String,
            default: '',
        },

        loading: {
            type: Boolean,
            default: false,
        },

        disableStyling: {
            type: Boolean,
            default: false,
        },
    },

    computed: {
        buttonClasses () {
            if (this.disableStyling)  {
                return {};
            }

            return {
                'focus:outline-none': true,
                'mx-0.5': true,
                'leading-normal': true,
                'w-6': true,
                'bg-red-500': this.active,
                'text-white bg-primary-dark border-soar-500': this.active,
                'cursor-default': this.active || this.disabled,
                'bg-gray-200': this.disabled && this.page !== '...',
                'text-gray': this.disabled && this.page !== '...',
                'hover:bg-gray-100': !this.active && !this.disabled,
            };
        },
    },

    methods: {
        pageChange () {
            if (
                this.page === '...' ||
                this.disabled ||
                this.active
            ) {
                return;
            }

            this.$emit('page-change');
        },
    },
};
</script>
