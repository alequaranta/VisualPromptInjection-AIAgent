package javalin;

import io.javalin.Javalin;
import io.javalin.http.staticfiles.Location;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.concurrent.atomic.AtomicInteger;

public class JavalinServer {
    private static final Map<String, String> ADVERTISEMENT_PAGES = Map.of(
            "1", "adv-1.html",
            "4", "adv-4.html"
    );
    private static final Map<String, AtomicInteger> CLICK_COUNTS = Map.of(
            "1", new AtomicInteger(),
            "4", new AtomicInteger()
    );

    public static void main(String[] args) {
        var app = Javalin.create(config -> {
            config.staticFiles.add(staticFiles -> {
                staticFiles.directory = "resources";
                staticFiles.location = Location.EXTERNAL;
            });
        }).start(8081);

        app.get("/", ctx -> ctx.redirect("/index.html"));
        app.get("/click/adv/{id}", ctx -> {
            var advertisementId = ctx.pathParam("id");
            var destination = ADVERTISEMENT_PAGES.get(advertisementId);

            if (destination == null) {
                ctx.status(404).result("Pubblicità non trovata.");
                return;
            }

            CLICK_COUNTS.get(advertisementId).incrementAndGet();
            ctx.redirect("/" + destination);
        });
        app.get("/api/clicks", ctx -> {
            var counts = new LinkedHashMap<String, Integer>();
            for (var advertisementId : ADVERTISEMENT_PAGES.keySet()) {
                counts.put("Pubblicità " + advertisementId, CLICK_COUNTS.get(advertisementId).get());
            }
            ctx.json(counts);
        });
    }
}
