import { expect, test } from "vitest";
import { mount } from "@vue/test-utils";
import HomeView from "../public/HomeView.vue";

test('HomeView.vue mount test', async () => {
    expect(HomeView).toBeTruthy();
});