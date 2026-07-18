# 16 - Spring Internals, Auto-Configuration, AOP, and Web Pipeline

## Why This Chapter Exists

At beginner level, Spring appears to “magically” create objects and apply annotations. There is no magic: Spring reads bean definitions, constructs objects, and sometimes returns a wrapper (proxy) that adds transactions, security, caching, or other behavior.

Read this chapter only after you can build and test a basic REST service.

## Application Context and Bean Lifecycle

Spring reads bean definitions, creates infrastructure processors, instantiates beans, injects dependencies, invokes lifecycle callbacks, and may wrap beans in proxies.

Important extension points:

- `BeanFactoryPostProcessor`: changes bean definitions before ordinary bean creation
- `BeanPostProcessor`: inspects or wraps bean instances
- `@PostConstruct`: initialization after injection
- `@PreDestroy`: cleanup before context shutdown
- `SmartLifecycle`: ordered start/stop for managed components

## Auto-Configuration

Boot auto-configuration uses conditions such as class presence, properties, web application type, and missing user beans.

```java
@Configuration(proxyBeanMethods = false)
@ConditionalOnClass(HttpClient.class)
@ConditionalOnMissingBean(RemoteGateway.class)
class GatewayAutoConfiguration {
    @Bean
    RemoteGateway remoteGateway() {
        return request -> "handled:" + request;
        // Result: bean is created only when HttpClient exists and no RemoteGateway is supplied.
    }
}
```

Use the conditions evaluation report to explain why an auto-configuration matched or did not match.

## Proxy-Based AOP

Spring commonly uses JDK dynamic proxies for interfaces or class-based proxies. Calls entering through the proxy can receive transaction, security, cache, async, or custom advice.

```java
@Aspect
@Component
final class TimingAspect {
    @Around("execution(* com.example.order..*Service.*(..))")
    Object measure(ProceedingJoinPoint joinPoint) throws Throwable {
        long started = System.nanoTime();
        try {
            return joinPoint.proceed();
        } finally {
            long elapsed = System.nanoTime() - started;
            System.out.println("elapsedNanos=" + elapsed);
            // Output: one non-negative elapsedNanos value per matched invocation.
        }
    }
}
```

Self-invocation bypasses proxy advice. Final/private methods and early construction can also prevent expected interception.

## Servlet Request Pipeline

```text
container -> Filter chain -> DispatcherServlet -> HandlerMapping -> HandlerInterceptor
-> argument resolvers/validation -> Controller -> return-value handlers -> message converter
# Result: an HTTP request becomes a validated controller call and serialized response.
```

- Filter: servlet-level request/response concerns such as correlation and security chain integration
- HandlerInterceptor: Spring MVC handler pre/post processing
- ControllerAdvice: controller exception/binding concerns
- AOP: method execution across Spring beans

## Scope Interview Points

- singleton: one bean instance per application context and bean definition
- prototype: new instance for each container lookup/injection resolution
- request/session: web-scoped instance

Injecting a prototype directly into a singleton resolves it once. Use an `ObjectProvider` only when a new instance is genuinely required per operation.
