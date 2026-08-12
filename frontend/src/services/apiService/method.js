import { publicApi, privateApi } from "./api";

const client = (auth = true) => (auth ? privateApi : publicApi);

/**
 * GET
 */
export const get = async ({
    path,
    params,
    headers,
    auth = false,
    signal,
}) => {
    const { data } = await client(auth).get(path, {
        params,
        headers,
        signal,
    });

    return data;
};

/**
 * POST
 */
export const post = async ({
    path,
    body,
    params,
    headers,
    auth = true,
    signal,
}) => {
    const { data } = await client(auth).post(path, body, {
        params,
        headers,
        signal,
    });

    return data;
};

/**
 * PUT
 */
export const put = async ({
    path,
    body,
    params,
    headers,
    auth = true,
    signal,
}) => {
    const { data } = await client(auth).put(path, body, {
        params,
        headers,
        signal,
    });

    return data;
};

/**
 * PATCH
 */
export const patch = async ({
    path,
    body,
    params,
    headers,
    auth = true,
    signal,
}) => {
    const { data } = await client(auth).patch(path, body, {
        params,
        headers,
        signal,
    });

    return data;
};

/**
 * DELETE
 */
export const remove = async ({
    path,
    body,
    params,
    headers,
    auth = true,
    signal,
}) => {
    const { data } = await client(auth).delete(path, {
        data: body,
        params,
        headers,
        signal,
    });

    return data;
};

