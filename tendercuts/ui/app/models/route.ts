export class Route {
    public route_distance: number;
    public route_duration: number;
    public orders: [Order];
}

export class Order {
    public order_long: number;
    public order_lat: number;
    public order_id: string;
}
