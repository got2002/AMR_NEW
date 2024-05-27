<template>
    <th 
        class="px-3 bg-theme-black-50 bg-opacity-50 text-sm font-bold text-theme-black-300 align-middle py-3"
        :class="{'text-left': align == 'left', 'text-center': align == 'center'}"
    >
        {{ text }}
    </th>
</template>

<script>
export default {
    props: {
        text: {
            type: String,
            required: true
        },
        align: {
            type: String,
            required: true
        }
    }
}
</script>