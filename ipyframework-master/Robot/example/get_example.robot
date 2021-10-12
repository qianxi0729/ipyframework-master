*** Settings ***
Documentation
...  测试get请求

Library  Env.environment
Library  Lib.CommonKeywords.RequestsKeywords  ${API_MAIN_URL}

*** Variables ***

*** Test Cases ***
Get请求测试
    ${response}  get  /about
    ${code}  get http code
    ${text}  get response text
    log to console  ${code}
    # log to console  ${text}
    # LOG   ${text}