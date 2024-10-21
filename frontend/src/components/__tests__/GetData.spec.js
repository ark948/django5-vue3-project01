import { expect, test } from "vitest";
import { mount } from "@vue/test-utils";
import GetData from "../GetData.vue";


test('GetData.vue mount test', async () => {
    expect(GetData).toBeTruthy();
    const wrapper = mount(GetData);
    expect(wrapper.get('[data-test="title"]').text()).toBe('Data:');
    expect(wrapper.get('[data-test="msg"]').text()).toBe("");
    expect(wrapper.get('[data-test="btn"').text()).toBe("Request data");
    await wrapper.get('[data-test="btn"]').trigger('click');
    expect(wrapper.get('[data-test="msg"]').text()).toBe("Hello");
    expect(wrapper.find('#nonExistentElem').exists()).toBe(false);
})