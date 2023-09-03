#include <stdlib.h>
#include <stdio.h>

#include <glog/logging.h>
#include <iostream>
#include <fstream>

//将信息输出到单独的文件和 LOG(ERROR)
void SignalHandle(const char *data, int size) {
    std::ofstream fs("glog_dump.log", std::ios::app);
    std::string str = std::string(data, size);
    fs << str;
    fs.close();
    LOG(ERROR) << str;
}

class GLogHelper {
        public:
        GLogHelper(const char *program) {
            google::InitGoogleLogging(program);
            FLAGS_colorlogtostderr = true;
            google::InstallFailureSignalHandler();
            //默认捕捉 SIGSEGV 信号信息输出会输出到 stderr，可以通过下面的方法自定义输出方式：
            google::InstallFailureWriter(&SignalHandle);

            google::SetLogDestination(google::GLOG_INFO, "./result_");
        }
        ~GLogHelper() {
            google::ShutdownGoogleLogging();
        }
};

void f1(void) {
    puts("pushed first");
}

void f2(void) {
    puts("pushed second");
}

int main(void) {
    GLogHelper gh("gh");

    atexit(f1);
    atexit(f2);

    abort();
//    exit(0);
}
