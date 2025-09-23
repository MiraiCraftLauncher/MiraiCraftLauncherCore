package net

import (
	"bytes"
	"context"
	"errors"
	"fmt"
	"net/http"
	"strings"
	"time"

	"github.com/MiraiCL/MiraiCL.Core/base/helper"
	"github.com/MiraiCL/MiraiCL.Core/base/internal"
)

var client = &http.Client{
	Timeout: time.Millisecond * time.Duration( 25000),
}

type HttpRequestBuilder struct {
	url     string
	method  string
	data    *bytes.Buffer
	headers map[string]string
	timeout uint16
	retry uint16
}

func NewHttpRequestBuilder(url string, method string) *HttpRequestBuilder {
	return &HttpRequestBuilder{
		url:     url,
		method:  method,
		data:    nil,
		headers: make(map[string]string),
	}
}

func (b *HttpRequestBuilder) AddHeader(key string, value string) *HttpRequestBuilder {
	b.headers[key] = value
	return b
}

func (b *HttpRequestBuilder) AddHeaders(keyValuePair map[string]string) *HttpRequestBuilder {
	for key, value := range keyValuePair {
		b.headers[key] = value
	}
	return b
}

func (b *HttpRequestBuilder) WithTimeout(keyValuePair map[string]string) *HttpRequestBuilder {
	for key, value := range keyValuePair {
		b.headers[key] = value
	}
	return b
}

func (b *HttpRequestBuilder) WithAuthorization(value string) *HttpRequestBuilder {
	b.headers["Authorization"] = value
	return b
}

func (b *HttpRequestBuilder) WithUserAgent(value string) *HttpRequestBuilder {
	b.headers["User-Agent"] = value
	return b
}

func (b *HttpRequestBuilder) WithStringContent(value string) *HttpRequestBuilder {
	b.data = bytes.NewBufferString(value)
	return b
}

func (b *HttpRequestBuilder) WithJSONContent(jsonStr string) *HttpRequestBuilder {
	b.data = bytes.NewBufferString(jsonStr)
	b.headers["Content-Type"] = "application/json"
	return b
}

func (b *HttpRequestBuilder) WithByteArrayContent(data *bytes.Buffer){
	b.data = data
}

func (b *HttpRequestBuilder) Build() (*http.Request, error) {
	b.secretSign()
	
	req, err := http.NewRequest(b.method, b.url, b.data)
	if err != nil {
		return nil, err
	}
	
	for key, value := range b.headers {
		req.Header.Set(key, value)
	}
	
	return req, nil
}

func (b *HttpRequestBuilder) Execute() (*http.Response, error) {
	req, err := b.Build()
	if err != nil {
		return nil, err
	}
	ctx ,cancel := context.WithTimeout(context.Background(),time.Duration(b.timeout)*time.Millisecond)
	defer cancel()
	req = req.WithContext(ctx)
	var lastError error
	for i:=0;i < int(b.retry);i++{
		resp,err := client.Do(req)
		if err != nil && errors.Is(err,context.DeadlineExceeded){
			lastError = err
			continue
		}
		return resp,nil
	}
	return nil,lastError
}

func (b *HttpRequestBuilder) secretSign() {
	if strings.Contains(b.url, "minecraftforge.net") {
		b.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
	}
	if strings.Contains(b.url, "api.curseforge.com") {
		b.headers["x-api-key"] = internal.CurseForgeApiKey
	}
	if helper.IsEmpty(b.headers["User-Agent"]) {
		b.headers["User-Agent"] = fmt.Sprintf(internal.UserAgent, internal.LauncherName, internal.Version)
	}
}

