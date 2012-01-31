import os

needed_env = ["ANDROID_PRODUCT_OUT", "ANDROID_EABI_TOOLCHAIN", "ANDROID_BUILD_TOP"]

# put your lib list here
libs = ["/system/lib/hw/camera.tegra.so", 
        "/system/lib/libnvmm_camera.so"]

if __name__ == "__main__":
    env = {}
    for v in needed_env:
        env[v] = os.getenv(v)
        
        if not env[v]:
            print "Missing environment variable: " + v
            sys.exit(0)

    os.system("adb remount")
    for lib in libs:
        pp = os.path.join(env["ANDROID_PRODUCT_OUT"], lib[1:])

        cmdline = "adb push %s %s" % (pp, os.path.dirname(lib)+"/")
        print cmdline
        os.system(cmdline)
