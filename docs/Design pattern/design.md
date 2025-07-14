

好的！用 C 语言实现设计模式的核心在于 **利用结构体（封装数据）和函数指针（封装行为）来模拟面向对象的关键特性（多态、封装、继承）**。以下是嵌入式开发中最常用、最易理解的设计模式总结，配合精简的 C 语言伪代码/思想：

---

### 1. 策略模式 (Strategy Pattern)
*   **目的：** **定义一系列算法，封装每个算法，并使它们可以互相替换。** 策略模式让算法独立于使用它的客户而变化。
*   **场景：** 需要多种方式完成同一任务（如不同加密算法、不同通信协议、不同传感器驱动、不同控制算法）。
*   **C 实现关键：**
    *   定义一个策略接口（结构体包含函数指针）。
    *   为每种具体策略实现该接口（定义结构体并实现函数）。
    *   客户端持有策略接口指针，运行时注入具体策略。
*   **精简 C 伪代码：**
    ```c
    // 1. 定义策略接口 (函数指针类型)
    typedef void (*SensorReadFunc)(void* context, float* result);
    
    // 2. 定义策略上下文结构体 (模拟"接口")
    typedef struct {
        void* sensorCtx;       // 具体传感器的上下文/数据
        SensorReadFunc read;   // 策略函数指针
    } SensorStrategy;
    
    // 3. 实现具体策略A: DS18B20
    void ds18b20_read(void* ctx, float* temp) {
        DS18B20_Data* data = (DS18B20_Data*)ctx;
        // 读取DS18B20硬件的代码...
        *temp = ...;
    }
    // 创建DS18B20策略对象
    SensorStrategy ds18b20_strategy = { &myDs18b20Data, ds18b20_read };
    
    // 4. 实现具体策略B: DHT11 (类似)
    void dht11_read(void* ctx, float* temp) { ... }
    SensorStrategy dht11_strategy = { &myDht11Data, dht11_read };
    
    // 5. 客户端使用 (不关心具体传感器)
    float currentTemp;
    SensorStrategy* activeSensor = &ds18b20_strategy; // 运行时可切换为 &dht11_strategy
    activeSensor->read(activeSensor->sensorCtx, &currentTemp); // 多态调用!
    ```
*   **优点:** 算法切换灵活、避免大量 `if-else`、符合开闭原则。

---

### 2. 观察者模式 (Observer Pattern)
*   **目的：** **定义对象间的一种一对多的依赖关系，当一个对象（Subject）状态改变时，所有依赖它的对象（Observers）都得到通知并自动更新。**
*   **场景：** 事件通知系统（按键检测、传感器数据更新、状态机状态改变）、GUI 更新。
*   **C 实现关键：**
    *   主题 (`Subject`) 维护一个观察者 (`Observer`) 列表（通常是链表）。
    *   观察者是一个包含更新函数指针的结构体。
    *   主题状态改变时，遍历列表调用所有观察者的更新函数。
*   **精简 C 伪代码：**
    ```c
    // 1. 定义观察者接口 (函数指针类型)
    typedef void (*UpdateFunc)(void* observerCtx, int newState);
    
    // 2. 观察者结构体
    typedef struct Observer {
        void* ctx;            // 观察者自身上下文
        UpdateFunc update;    // 更新回调函数
        struct Observer* next; // 链表指针
    } Observer;
    
    // 3. 主题结构体
    typedef struct {
        int state;
        Observer* observerList; // 观察者链表头
    } Subject;
    
    // 4. 主题注册观察者
    void subject_attach(Subject* sub, Observer* obs) {
        // 将obs添加到sub->observerList链表
    }
    
    // 5. 主题状态改变并通知
    void subject_setState(Subject* sub, int newState) {
        sub->state = newState;
        Observer* current = sub->observerList;
        while (current != NULL) {
            current->update(current->ctx, newState); // 通知所有观察者!
            current = current->next;
        }
    }
    
    // 6. 具体观察者实现 (例如: LED控制器)
    void led_update(void* ctx, int state) {
        LED_Controller* led = (LED_Controller*)ctx;
        if (state == 1) led_turnOn(led);
        else led_turnOff(led);
    }
    // 创建LED观察者
    Observer led_observer = { &myLed, led_update };
    
    // 7. 使用
    Subject mySubject;
    subject_attach(&mySubject, &led_observer);
    subject_setState(&mySubject, 1); // LED会亮起
    ```
*   **优点：** 松耦合（主题不知道观察者细节）、支持广播通信、动态添加/移除观察者。
*   **注意：** C 中需小心管理观察者生命周期（注销时要从链表移除）。

---

### 3. 工厂模式 (简单工厂/Factory Method)
*   **目的：** **定义一个用于创建对象的接口，让子类决定实例化哪一个类。工厂方法使一个类的实例化延迟到其子类。** (简单工厂是简化版，非 GoF 23 种之一，但嵌入式常用)。
*   **场景：** 需要根据配置或条件创建不同类型但接口一致的对象（如创建不同型号的传感器驱动、不同通信接口对象）。
*   **C 实现关键 (简单工厂)：**
    *   定义一个产品接口（结构体+函数指针）。
    *   实现具体产品。
    *   创建一个工厂函数，根据输入参数 `new` 出具体产品并返回其接口指针。
*   **精简 C 伪代码 (简单工厂)：**
    ```c
    // 1. 产品接口 (传感器)
    typedef struct Sensor {
        void* sensorData;
        SensorReadFunc read;
    } Sensor;
    
    // 2. 具体产品A: DS18B20
    Sensor* create_ds18b20() {
        Sensor* s = malloc(sizeof(Sensor));
        s->sensorData = malloc(sizeof(DS18B20_Data));
        init_ds18b20(s->sensorData);
        s->read = ds18b20_read_func; // 实现read的函数
        return s;
    }
    // 3. 具体产品B: DHT11 (类似)
    Sensor* create_dht11() { ... }
    
    // 4. 简单工厂函数
    Sensor* sensor_factory(const char* type) {
        if (strcmp(type, "DS18B20") == 0) return create_ds18b20();
        else if (strcmp(type, "DHT11") == 0) return create_dht11();
        else return NULL; // 或默认
    }
    
    // 5. 客户端使用
    Sensor* mySensor = sensor_factory("DS18B20");
    float temp;
    mySensor->read(mySensor->sensorData, &temp);
    ```
*   **优点：** 将对象创建逻辑集中化、客户端与具体产品类解耦、易于扩展新产品（只需修改工厂函数）。

---

### 4. 单例模式 (Singleton Pattern)
*   **目的：** **保证一个类仅有一个实例，并提供一个访问它的全局访问点。**
*   **场景：** 需要严格唯一实例的资源（如系统状态管理器、硬件抽象层 HAL、日志记录器、配置管理器）。
*   **C 实现关键：**
    *   将实例定义为 `static` 变量（藏在 .c 文件内）。
    *   提供一个全局访问函数 (`getInstance()`)。
    *   在访问函数内初始化该 `static` 实例（通常只初始化一次）。
*   **精简 C 伪代码：**
    ```c
    // singleton.h (对外接口)
    typedef struct {
        // ... 单例的数据和方法 (函数指针)
        void (*doSomething)(void);
    } Singleton;
    
    Singleton* get_singleton_instance(void);
    
    // singleton.c (实现)
    #include "singleton.h"
    
    static Singleton instance; // 唯一实例, static 隐藏!
    
    // 初始化函数 (内部或由get_instance调用)
    static void singleton_init(Singleton* s) {
        // 初始化s的数据成员...
        s->doSomething = &real_do_something;
    }
    
    Singleton* get_singleton_instance(void) {
        static int initialized = 0;
        if (!initialized) {
            singleton_init(&instance);
            initialized = 1;
        }
        return &instance;
    }
    
    // 客户端使用
    Singleton* globalState = get_singleton_instance();
    globalState->doSomething();
    ```
*   **优点：** 严格控制唯一实例、全局访问点。
*   **注意：** 嵌入式环境中需考虑 **线程安全**（如果有多任务）。简单方案可在 `get_instance` 内加锁（如果 OS 支持），或确保在单一线程初始化。

---

### 5. 适配器模式 (Adapter Pattern)
*   **目的：** **将一个类的接口转换成客户希望的另外一个接口。** 使原本接口不兼容的类可以一起工作。
*   **场景：** 集成第三方库/旧代码、统一不同硬件模块的接口（如不同厂家显示屏驱动适配到统一图形接口）、协议转换。
*   **C 实现关键 (对象适配器)：**
    *   定义目标接口 (`Target`)，即客户端期望的接口。
    *   创建适配器类 (`Adapter`)，它包含一个被适配者 (`Adaptee`) 的实例指针。
    *   在适配器中实现 `Target` 接口，其方法内部调用 `Adaptee` 的特定方法（可能进行转换）。
*   **精简 C 伪代码 (统一显示接口)：**
    ```c
    // 1. 目标接口 (期望的显示屏驱动)
    typedef struct DisplayTarget {
        void (*drawPixel)(int x, int y, int color);
    } DisplayTarget;
    
    // 2. 被适配者A: OLED库 (接口不同)
    typedef struct {
        void (*oledSetPixel)(uint8_t col, uint8_t page, uint8_t bit);
    } OLED_Driver;
    
    // 3. 适配器 (让OLED看起来像DisplayTarget)
    typedef struct {
        DisplayTarget target;     // "继承"目标接口 (组合)
        OLED_Driver* oledDriver; // 持有被适配者
    } OLED_Adapter;
    
    // 4. 实现适配器的目标接口方法
    void oledAdapter_drawPixel(int x, int y, int color) {
        OLED_Adapter* adapter = ...; // 获取适配器上下文 (常用技巧: 函数第一个参数是this指针)
        // 将标准x,y,color转换为OLED库需要的col, page, bit格式
        uint8_t col = x / 8;
        uint8_t page = y / 8;
        uint8_t bit = 1 << (y % 8);
        adapter->oledDriver->oledSetPixel(col, page, (color) ? bit : 0);
    }
    
    // 5. 创建并初始化适配器
    OLED_Driver myOled;
    OLED_Adapter oledAdapter;
    oledAdapter.target.drawPixel = oledAdapter_drawPixel;
    oledAdapter.oledDriver = &myOled;
    
    // 6. 客户端使用目标接口 (不知道背后是OLED)
    DisplayTarget* myDisplay = (DisplayTarget*)&oledAdapter;
    myDisplay->drawPixel(10, 20, 1); // 实际调用适配器转换后的代码
    ```
*   **优点：** 复用现有类、让不兼容接口协同工作、提高灵活性。

---

### 总结表 (嵌入式 C 视角)

| 模式       | 核心目的         | 嵌入式典型应用场景             | C 实现关键点                                  |
| :--------- | :--------------- | :----------------------------- | :-------------------------------------------- |
| **策略**   | 封装可互换的算法 | 多驱动支持 (传感器/通信/控制)  | **结构体(接口) + 函数指针数组/结构体成员**    |
| **观察者** | 一对多状态通知   | 事件处理 (按键/传感器/状态机)  | **链表 + 回调函数指针**                       |
| **工厂**   | 封装对象创建     | 动态创建驱动/组件              | **创建函数 + `switch`/表驱动 + 返回接口指针** |
| **单例**   | 保证全局唯一实例 | HAL/状态管理/日志/配置         | **`static` 全局实例 + 获取函数**              |
| **适配器** | 转换不兼容接口   | 集成旧库/统一硬件接口/协议转换 | **组合被适配者 + 实现目标接口(转换调用)**     |

**重要提示：**

1.  **C 非 OOP 语言：** 这些实现是**模拟**设计模式思想，代码结构会比 Java/C++ 更显式、更底层（需要手动管理 `this` 指针、生命周期、链表等）。
2.  **函数指针是核心：** 它们是实现多态（运行时绑定）的关键。
3.  **结构体封装数据：** 将数据和操作它的函数（指针）组织在一起模拟“对象”。
4.  **`void*` 上下文：** 广泛用于传递“对象”自身的上下文 (`this` 指针)。
5.  **内存管理：** 嵌入式中需谨慎使用动态内存 (`malloc/free`)，工厂模式、观察者链表等尤其注意。尽量使用静态内存池或提前分配。
6.  **模式是工具：** **不要为了用模式而用模式！** 评估复杂度是否值得引入模式。嵌入式开发中，策略、观察者、适配器、简单工厂最为常用和实用。

理解这些模式的思想（解耦、复用、扩展）比死记硬背代码更重要。在实际项目中识别出适用场景，再用 C 的这些技巧去实现，才能真正提升代码质量。