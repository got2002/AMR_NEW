<template>
    <th 
        class="px-3 bg-aerothai text-xs text-gray-200 align-middle border border-solid border-gray-100 py-3 uppercase border-r-2 whitespace-nowrap font-medium"
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